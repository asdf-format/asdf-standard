.. _resources:

ASDF Standard Resources
=======================

The included schema and manifest resources made available by the ASDF-standard are described below.

.. _schema:

ASDF Standard Schema Definitions
--------------------------------

ASDF schemas are arranged into "modules".  All ASDF implementations
must support the "core" module, but the other modules are optional.

.. toctree::
   :maxdepth: 2

   core.rst
   unit.rst
   legacy.rst

The ASDF Standard also defines two meta-schemas that are used for validating
the ASDF schemas themselves. These schemas are useful references when creating
custom schemas (see `extending-asdf`).

.. toctree::
   :maxdepth: 0

   yaml_schema.rst

.. asdf-autoschemas::

   asdf-schema-1.0.0

The following graph shows the dependencies between modules:

.. digraph:: modules

   "fits" -> "core"
   "unit" -> "core"
   "time" -> "core"
   "core" -> "unit"

.. _manifest:

.. include:: manifest.rst
