1.1.1 (unreleased)
------------------

-

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
