1.1.0 (unreleased)
------------------

The in progress ASDF Standard is v1.6.0

The stable ASDF Standard is v1.5.0

- Remove ``fits-1.0.0`` schema completely, in favor of it being in the separate
  ``asdf-fits-schemas`` package. [#338]
- Remove ``wcs`` schemas completely, in favor of all of them being in the separate
  ``asdf-wcs-schemas`` package. [#340]
- Remove ``time-1.0.0``, ``time-1.1.0``, and ``time-1.2.0`` schemas completely,
  in favor of them being in the separate ``asdf-time-schemas`` package. [#339]

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
