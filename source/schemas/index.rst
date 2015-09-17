.. _schema:

ASDF schema definitions
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
   wcs.rst

The following graph shows the dependencies between modules:

.. digraph:: modules

   "fits" -> "core"
   "unit" -> "core"
   "time" -> "core"
   "transform" -> "core"
   "wcs" -> "transform"
   "wcs" -> "unit"
   "wcs" -> "time"
