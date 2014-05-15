.. _extending-finf:

Extending FINF
==============

FINF is designed to be extensible so outside teams can add their own
types and structures while retaining compatibility with tools that
don't understand those conventions.

TODO: This section will describe making a custom tag type for FINF.

.. _yaml-schema:

YAML Schema
-----------

YAML Schema is a small extension to `JSON Schema Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__ created
specifically for FINF.  `Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__
provides a good resource for understanding how to use JSON Schema, and
further resources are available at `json-schema.org
<http://json-schema.org>`__.  This section describes what makes YAML
Schema different from JSON Schema, and provides some examples in the
context of FINF.

Writing a new schema is described in :ref:`extending-finf`.

New keywords
^^^^^^^^^^^^

YAML Schema adds two new keywords to JSON Schema.

- ``tag``, which may be attached to any data type, declares that the
  element must have the given YAML tag.  For example, TODO

- ``propertyOrder``, which applies only to objects, declares that the
  object must have its properties presented in the given order.  For
  example, TODO
