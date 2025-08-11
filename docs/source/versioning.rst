.. _versioning-conventions:

Versioning Conventions
======================

One of the explicit goals of ASDF is to be as future proof as
possible.  This involves being able to add features as needed while
still allowing older libraries that may not understand those new
features to reasonably make sense of the rest of the file.

ASDF makes extensive use of versioning to retain backwards compatibility
and as a result many version numbers will be encountered for even
just a single ASDF file.

An ASDF file may have several versions:

- **File format version**: Refers to the version of the blocking
  scheme and other details of the low-level file layout.  This is the
  number that appears on the ``#ASDF`` header line at the start of
  every ASDF file and is essential to correctly interpreting the
  various parts of an ASDF file.

- **Standard version**: The version of the standard/specification as a whole.
  This version provides a convenient handle to refer to a particular
  snapshot of the ASDF specification at a given time.  This allows
  libraries to advertise support for "ASDF specification version X.Y.Z".

- **Tag versions**: Rich data structures are "tagged" (a concept inherited
  from YAML). These tags are versioned to allow ASDF to read and
  validate old file even if newer versions of the tag (which may
  link to a new schema) are available.

- **Schema versions**: Each schema (that may correspond to a YAML tag)
  is individually versioned.  This allows schemas to evolve, while still
  allowing data written with an older version of the schema to be
  validated correctly.

- **Extension versions**: Schemas and tags added to ASDF via extensions
  are versioned to aid in backwards compatibility.

- **Package versions**: Schemas might be provided via a package
  distribution system (such as pypi in Python). The version of a
  package that provides schemas might not match the versions of the
  schemas in the package.

Consider the following ASDF file:

.. code-block:: yaml

   #ASDF 1.0.0
   #ASDF_STANDARD 1.6.0
   %YAML 1.1
   %TAG ! tag:stsci.edu:asdf/
   --- !core/asdf-1.1.0
   asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
     name: asdf, version: 4.1.0}
   history:
     extensions:
     - !core/extension_metadata-1.0.0
       extension_class: asdf.extension._manifest.ManifestExtension
       extension_uri: asdf://asdf-format.org/core/extensions/core-1.6.0
       manifest_software: !core/software-1.0.0 {name: asdf_standard, version: 1.1.1}
       software: !core/software-1.0.0 {name: asdf, version: 4.1.0}
   data: !core/ndarray-1.1.0
     data: [0, 1, 2, 3, 4, 5, 6, 7]
     datatype: int64
     shape: [8]
   ...

In the above example we find:

* File format version 1.0.0
* Specification/standard version 1.6.0
* a ``data`` key tagged with ``ndarray`` tag version 1.1.0
* an extension ``core-1.6.0`` that was used while writing this file
* a package ``asdf_standard`` versioned 1.1.1 which provided the ``core-1.6.0`` extension manifest
* a package ``asdf`` versioned 4.1.0 which implemented the support for the ``core-1.6.0`` extension

Version numbers all follow the same convention according to the
`Semantic Versioning 2.0.0 <http://semver.org/spec/v2.0.0.html>`__
specification.

- **major version**: The major version number advances when a
  backward incompatible change is made.  For example, this would
  happen when an existing property in a schema changes meaning.
  (An exception to this is that when the major version is 0, there
  are no guarantees of backward compatibility.)

- **minor version**: The minor version number advances when a
  backward compatible change is made.  For example, this would
  happen when new properties are added to a schema.

- **patch version**: The patch version number advances when a minor
  change is made that does not directly affect the file format itself.
  For example, this would happen when a misspelling or grammatical
  error in the specification text is made that does not affect the
  interpretation of an ASDF file.

- **pre-release version**: An optional fourth part may also be present
  following a hyphen to indicate a pre-release version in development.
  For example, the pre-release of version ``1.2.3`` would be
  ``1.2.3-dev+a2c4``.

Handling version mismatches
---------------------------

Given the variety of versions it is important to consider how an
ASDF implenentation will handle version mismatches.
ASDF implementations should, but are not required, to
support as many existing versions of the file format and schemas as
possible, and use the version numbers in the file to act accordingly.

If while reading a file an unknown version number is encountered
the library should warn the user and must return a structure that
preserves the version information but does not deserialize the
versioned object.

For example if the ``foo-1.1.0`` tag is known and
a file contains a ``foo-1.0.0`` tag the unknown ``1.0.0`` version
must not be handled like a ``foo-1.1.0`` object. The same
is true if the file contains a newer but still unknown version
(for example ``foo-2.0.0``). This behavior applies to tags
that differ by any element (major, minor or patch) of the version
number.

When writing ASDF files, it is recommended that libraries provide both
of the following modes of operation:

- Upgrade the file to the latest versions of the file format and
  schemas understood by the library.

- Preserve the version of the ASDF specification used by the input file.

Writing out a file that mixes versions of schema from different
versions of the ASDF core schemas is not recommended, though such a file
should be accepted by readers given the rules above.
