.. _resources:

ASDF Specification Resources
============================

The included schema and manifest resources made available by the ASDF are described below.

.. _schema:

ASDF Specification Schema Definitions
-------------------------------------

ASDF schemas are arranged into "modules".  All ASDF implementations
must support the "core" module, but the other modules are optional.

.. toctree::
   :maxdepth: 2

   core.rst
   astronomy.rst
   legacy.rst

The ASDF Specification also defines a meta-schema that is useful for validating
the ASDF schemas themselves. These schemas are useful references when creating
custom schemas (see `extending-asdf`).

.. toctree::
   :maxdepth: 0

   yaml_schema.rst

.. _manifest:

.. include:: manifest.rst
