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
   fits.rst
   unit.rst
   time.rst
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

ASDF Standard Manifests
-----------------------

The ASDF tags (described by schemas) available under each ASDF standard version are all described
by a single manifest document for that ASDF standard version.

.. asdf-autoschemas::
   :schema_root: ../../resources/manifests
   :standard_prefix: asdf-format.org/core

   core-1.0.0
   core-1.1.0
   core-1.2.0
   core-1.3.0
   core-1.4.0
   core-1.5.0
   core-1.6.0
