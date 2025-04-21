.. _yaml-schema:

YAML Schema
===========

:ref:`YAML Schema <yaml-schema-draft-01>` is a small extension to `JSON Schema
Draft 4 <https://json-schema.org/draft-04/schema>`__ that
adds some features specific to YAML.  Resources for understanding JSON schema
are available at `json-schema.org <http://json-schema.org>`__.  A working
understanding of JSON Schema is assumed for this section, which only describes
what makes YAML Schema different from JSON Schema.

Writing a new schema is described in :ref:`extending-asdf`.

.. note::

   The YAML Schema currently does not require either the ``id`` or ``tag``
   keywords. The ``id`` keyword is not included in the YAML Schema since it is
   actually inherited from the base JSON Schema standard. However, it may
   become mandatory in a future version of the YAML Standard. The ``tag``
   keyword may also eventually become mandatory, although the motivation for
   this is somewhat weaker.

.. warning::

   This is a metaschema that extends another metaschema, a process
   that involves many advanced JSON schema techniques. Creation of
   new custom metaschemas is highly discouraged as these are poorly
   supported by many JSON schema libraries.

.. _yaml-schema-draft-01:

.. asdf-schema::
   :schema_root: ../../resources/schemas/stsci.edu
   :standard_prefix:

   yaml-schema/draft-01
