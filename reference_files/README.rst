This directory contains reference ADSF files.  ASDF parser
implementations are encouraged to use these files as part of their
test suite.

There is a directory here for each version of the ASDF standard.
They contain pairs of files: one ``.asdf`` file and one ``.yaml`` file.

To use the reference file suite, load the ``.asdf`` file and perform
the following transformations:

    - Convert all ``core/ndarray`` tags to in-line YAML data.

    - Load and store inline all ``JSON Pointer`` references.

    - Dereference all YAML aliases to anchors.

Compare the result to the matching ``.yaml`` file.  For compliance,
the files do not need to be byte-for-byte identical, but should
represent the same values at the YAML level.
