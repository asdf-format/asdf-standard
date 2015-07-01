.. _versioning-conventions:

Versioning Conventions
======================

One of the explicit goals of ASDF is to be as future proof as
possible.  This involves being able to add features as needed while
still allowing older libraries that may not understand those new
features to reasonably make sense of the rest of the file.

The ASDF standard includes three categories of versions, which all
advance independently of one another.

- The version of the standard as a whole.  This version does not
  appear in ASDF files, but provides a convenient handle to refer to a
  particular snapshot of the ASDF standard at a given time.  This
  allows libraries to advertise support for "ASDF standard version
  X.Y.Z".

- The file format version.  This appears in the ``#ASDF`` header line
  at the start of every ASDF file.  This version refers to details
  about the low-level file layout, including the contents of the block
  headers.

- Schema versions.  Each schema for a particular YAML tag is
  individually versioned.

Version numbers themselves all follow the same convention, and follows
the `Semantic Versioning 2.0.0 <http://semver.org/spec/v2.0.0.html>`__
specification.

- **major version**: The major version number advances when a
  backward incompatible change is made.  For example, this would
  happen when an existing property in a schema changes meaning.

- **minor version**: The minor version number advances when a
  backward compatible change is made.  For example, this would
  happen when new properties are added to a schema.

- **patch version**: The patch version number advances when a minor
  change is made that does not directly affect the file format itself.
  For example, this would happen when a misspelling or grammatical
  error in the text is made.

- **pre-release version**: An optional fourth part may also be present
  following a hyphen to indicate a pre-release version in development.
  For example, the pre-release of version ``1.2.3`` would be
  ``1.2.3-dev+a2c4``.

The version of the standard is incremented based on the the change of
version in the file format or the schemas.  For example, if any of the
schemas introduced a backward-incompatible change in a particular
release of the standard, the major number of the standard's version
would advance.

Handling version mismatches
---------------------------

Given these conventions, the ASDF standard recommends certain behavior
of ASDF libraries.  ASDF libraries should endeavour to support as many
existing versions of the file format and schemas as possible, and use
the version numbers in the file to act accordingly.  To help libraries
support older ASDF files, each ASDF standard release includes all
previously-released schemas (except those that differ only in the
patch version number).

For future proofing, the library should gracefully handle version
numbers that are greater than those understood by the library.

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

- Preserve the versions of the file format and schemas of the input
  file.
