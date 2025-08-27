1.5.0 (unreleased)
------------------

- Add missing transform-1.0.0 and domain-1.0.0 schemas.
  These are only used by legacy schemas and are not to be
  used for new schemas. See asdf-transform-schemas for
  newer versions of these schemas [#485]

1.4.0 (2025-08-27)
------------------

- Update documentation to use new terminology. The
  ASDF specification refers to the description of the file
  format whereas the ASDF core schemas refers to the versioned
  collection of schemas for core objects (ndarray, software, etc) [#473]
- Add datatype-1.0.0 schema [#455]
- Add galexsec time to time-1.4.0 [#480]

1.3.0 (2025-06-11)
------------------

- Add utime and tai_seconds formats to new time-1.3.0 [#461]

1.2.0 (2025-05-21)
------------------

- Update reference files [#409]
- Remove statement discouraging use of YAML anchors and aliases [#443]
- Documentation theme config changes for new ASDF website [#447]
- Adds global navigation in docs top bar [#448]
- Adds reference files for v1.6.0 [#439]
- Adds anchor, endian, structured and scalar reference files [#439]
- Update documentation to improve readability [#456]
- Discourage creation of new custom metaschemas [#456]
- Clarify that schema refs cannot contain tags [#456]
- Describe implementation handling of block compression identifiers [#456]
- Update description of how tag version mismatches should be handled [#456]
- Remove outdated schema top level tag attribute description [#456]
- Clarify post-tree pre-block padding allowed bytes [#456]

1.1.1 (2024-03-06)
------------------

- Fix readthedocs config. [#429]

1.1.0 (2024-03-05)
------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Add new ``quantity-1.2.0`` schema to support ``datatype`` option. [#351]
- Bugfix for ``base_format`` in ``time-1.2.0`` schema. [#349]
- Add new ``ndarray-1.1.0`` schema to fix #345 [#350]
- Remove ``unit-1.1.0`` erroneously added in #350 [#355]
- Fix URI fragment format in metaschema references. [#373]
- Fix URI fragment format in quantity-1.2 schema [#374]
- Drop support for python 3.8 [#390]
- Add ``float16`` to ``ndarray-1.1.0`` [#411]
- Remove unneeded ``tag`` keyword from ``fits`` schema [#421]
- Move non-core tags to ``astronomy`` manifest [#422]

1.0.3 (2022-08-08)
------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Update documentation to be consistent with the ASDF library documentation. [#316]
- Add ``time-1.2.0`` schema to document bugfix requiring additional property to be
  written from ``asdf-astropy``. [#319]
- Move packaging to ``pyproject.toml`` file from ``setup.cfg`` and ``setup.py``
  files. [#321]
- Remove ``tag`` from within the ``time-1.1.0`` schema. [#323]
- Remove ``tag`` from within the remaining schemas. [#326]

1.0.2 (2022-04-15)
------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Pin astropy min version to 5.0.4. [#310]

1.0.1 (2022-02-23)
------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Remove asdf as an install dependency for the asdf-standard package. [#300]

1.0.0 (2022-02-14)
-------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Add installable Python package to replace use of this repo as a submodule.  [#292]
