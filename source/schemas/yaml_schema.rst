.. _yaml-schema:

YAML Schema
===========

.. toctree::
   :hidden:

   schemas/stsci.edu/yaml-schema/draft-01.rst

:ref:`YAML Schema <http://stsci.edu/schemas/yaml-schema/draft-01>` is
a small extension to `JSON Schema Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__ that
adds some features specific to YAML..  `Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__
provides a good resource for understanding how to use JSON Schema, and
further resources are available at `json-schema.org
<http://json-schema.org>`__.  A working understanding of JSON Schema
is assumed for this section, which only describes what makes YAML
Schema different from JSON Schema.

Writing a new schema is described in :ref:`designing-schema`.

``tag`` keyword
^^^^^^^^^^^^^^^

``tag``, which may be attached to any data type, declares that the
element must have the given YAML tag.

For example, the root :ref:`asdf <core/asdf-1.1.0>` schema declares that
the ``data`` property must be an :ref:`ndarray <core/ndarray-1.0.0>`.  It does
this not by using the ``tag`` keyword directly, but by referencing the
``ndarray`` schema, which in turn has the ``tag`` keyword.  The ASDF schema
includes::

    properties:
      data:
        $ref: "ndarray"

And the :ref:`ndarray <core/ndarray-1.0.0>` schema includes::

    tag: "tag:stsci.edu:asdf/core/ndarray-1.0.0"

This has the net effect of requiring that the ``data`` property at the
top-level of all ASDF files is tagged as
``tag:stsci.edu:asdf/core/ndarray-1.0.0``.

``propertyOrder`` keyword
^^^^^^^^^^^^^^^^^^^^^^^^^

``propertyOrder``, which applies only to objects, declares that the
object must have its properties presented in the given order.

TBD: It is not yet clear whether this keyword is necessary or desirable.

``flowStyle`` keyword
^^^^^^^^^^^^^^^^^^^^^

Must be either ``block`` or ``flow``.

Specifies the default serialization style to use for an array or
object.  YAML supports multiple styles for arrays/sequences and
objects/maps, called "block style" and "flow style".  For example::

  Block style: !!map
   Clark : Evans
   Ingy  : döt Net
   Oren  : Ben-Kiki

  Flow style: !!map { Clark: Evans, Ingy: döt Net, Oren: Ben-Kiki }

This property gives an optional hint to the tool outputting the YAML
which style to use.  If not provided, the library is free to use
whatever heuristics it wishes to determine the output style.  This
property does not enforce any particular style on YAML being parsed.

``style`` keyword
^^^^^^^^^^^^^^^^^

Must be ``inline``, ``literal`` or ``folded``.

Specifies the default serialization style to use for a string.  YAML
supports multiple styles for strings::

  Inline style: "First line\nSecond line"

  Literal style: |
    First line
    Second line

  Folded style: >
    First
    line

    Second
    line

This property gives an optional hint to the tool outputting the YAML
which style to use.  If not provided, the library is free to use
whatever heuristics it wishes to determine the output style.  This
property does not enforce any particular style on YAML being parsed.

``examples`` keyword
^^^^^^^^^^^^^^^^^^^^

The schema may contain a list of examples demonstrating how to use the
schema.  It is a list where each item is a pair.  The first item in
the pair is a prose description of the example, and the second item is
YAML content (as a string) containing the example.

For example::

  examples:
    -
      - Complex number: 1 real, -1 imaginary
      - "!complex 1-1j"
