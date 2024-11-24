.. _yaml_schema:


YAML Schema
===========

:ref:`YAML Schema <yaml-schema-draft-01>` is a small extension to `JSON Schema
Draft 4 <http://json-schema.org/draft-04/json-schema-validation.html>`__ that
adds some features specific to YAML.  `Understanding JSON Schema
<https://json-schema.org/understanding-json-schema>`__ provides a good
resource for understanding how to use JSON Schema, and further resources are
available at `json-schema.org <http://json-schema.org>`__.  A working
understanding of JSON Schema is assumed for this section, which only describes
what makes YAML Schema different from JSON Schema.

Writing a new schema is described in :ref:`designing-new-schema`.

.. note::

   The YAML Schema currently does not require either the ``id`` or ``tag``
   keywords. The ``id`` keyword is not included in the YAML Schema since it is
   actually inherited from the base JSON Schema standard. However, it may
   become mandatory in a future version of the YAML Standard. The ``tag``
   keyword may also eventually become mandatory, although the motivation for
   this is somewhat weaker.
   


.. _yaml-schema-draft-01:


.. asdf-schema::
   :schema_root: ../../resources/schemas/stsci.edu
   :standard_prefix:

   yaml-schema/draft-01
