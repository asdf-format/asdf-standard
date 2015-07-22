.. _versioning-conventions:

Versioning Conventions
======================

One of the explicit goals of ASDF is to be as future proof as
possible.  This involves being able to add features as needed while
still allowing older libraries that may not understand those new
features to reasonably make sense of the rest of the file.

The ASDF standard includes three categories of versions, all of which
may advance independently of one another.

- **Standard version**: The version of the standard as a whole.  This
  version provides a convenient handle to refer to a particular
  snapshot of the ASDF standard at a given time.  This allows
  libraries to advertise support for "ASDF standard version X.Y.Z".

- **File format version**: Refers to the version of the blocking
  scheme and other details of the low-level file layout.  This is the
  number that appears on the ``#ASDF`` header line at the start of
  every ASDF file and is essential to correctly interpreting the
  various parts of an ASDF file.

- **Schema versions**: Each schema for a particular YAML tag is
  individually versioned.  We encourage schemas provided by third
  parties (i.e. not in the ASDF specification itself) to be versioned
  as well.

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

Relationship of version numbers
-------------------------------

The major number in the **standard version** is incremented whenever
the major number in the **file format version** is incremented.

At present the **schema versions** move in lock-step with the
**standard version**.  However, in the future, we may break from that
convention, so libraries should address versions of individual schemas
independently.

Handling version mismatches
---------------------------

Given these conventions, the ASDF standard recommends certain behavior
of ASDF libraries.  ASDF libraries should, but are not required, to
support as many existing versions of the file format and schemas as
possible, and use the version numbers in the file to act accordingly.

For future proofing, the library should gracefully handle version
numbers that are greater than those understood by the library.  The
following applies to both kinds of version numbers that appear in the
file: the **file format version** and **schema versions**.

- When encountering a **major version** that is greater than the
  understood version, by default, an exception should be raised.  This
  behavior may be overridden through explicit user interaction, in
  which case the library will attempt to handle the element using the
  conventions of the most recent understood version.

- When encountering a **minor version** that is greater than the
  understood version, a warning should be emitted, and the library
  should attempt to handle the element using the conventions of the
  most recent understood version.

- When encountering a **patch version** that is greater than the
  understood version, silently ignore the difference and handle the
  element using the conventions of the most recent understood version.

When writing ASDF files, it is recommended that libraries provide both
of the following modes of operation:

- Upgrade the file to the latest versions of the file format and
  schemas understood by the library.

- Preserve the version of the ASDF standard used by the input file.

Writing out a file that mixes versions of schema from different
versions of the ASDF standard is not recommended, though such a file
should be accepted by readers given the rules above.
