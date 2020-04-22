.. _schema:

ASDF Schema Definitions
=======================

This reference section describes the schema files for the built-in
tags in ASDF.

ASDF schemas are arranged into "modules".  All ASDF implementations
must support the "core" module, but the other modules are optional.

.. toctree::
   :maxdepth: 2

   core.rst
   fits.rst
   unit.rst
   time.rst
   transform.rst

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
   "transform" -> "core"
   "wcs" -> "transform"
   "wcs" -> "unit"
   "wcs" -> "time"
