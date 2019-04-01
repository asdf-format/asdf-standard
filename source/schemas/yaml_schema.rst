.. _yaml-schema:

YAML Schema
===========

:ref:`YAML Schema <yaml-schema-draft-01>` is a small extension to `JSON Schema
Draft 4 <http://json-schema.org/draft-04/json-schema-validation.html>`__ that
adds some features specific to YAML.  `Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__ provides a good
resource for understanding how to use JSON Schema, and further resources are
available at `json-schema.org <http://json-schema.org>`__.  A working
understanding of JSON Schema is assumed for this section, which only describes
what makes YAML Schema different from JSON Schema.

Writing a new schema is described in :ref:`designing-schema`.

.. _yaml-schema-draft-01:

.. asdf-schema::
   :schema_root: ../schemas/stsci.edu
   :standard_prefix:

   yaml-schema/draft-01
