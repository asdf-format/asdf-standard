.. _extending-asdf:

Extending ASDF
==============

ASDF is designed to be extensible so outside teams can add their own
types and structures while retaining compatibility with tools that
don't understand those conventions.

.. _yaml-schema:

YAML Schema
-----------

YAML Schema is a small extension to `JSON Schema Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__ created
specifically for ASDF.  `Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__
provides a good resource for understanding how to use JSON Schema, and
further resources are available at `json-schema.org
<http://json-schema.org>`__.  A working understanding of JSON Schema
is assumed for this section, which only describes what makes YAML
Schema different from JSON Schema.

Writing a new schema is described in :ref:`designing-schema`.

YAML Schema adds three new keywords to JSON Schema.

``tag`` keyword
^^^^^^^^^^^^^^^

``tag``, which may be attached to any data type, declares that the
element must have the given YAML tag.

For example, the root :ref:`ASDF schema
<http://stsci.edu/schemas/asdf/0.1.0/core/asdf>` declares that
the ``data`` property must be an :ref:`ndarray
<http://stsci.edu/schemas/asdf/0.1.0/core/ndarray>`.  It does
this not by using the ``tag`` keyword directly, but by referencing the
``ndarray`` schema, which in turn has the ``tag`` keyword.  The `ASDF
schema` includes::

    properties:
      data:
        $ref: "ndarray"

And the `ndarray` schema includes::

    tag: "tag:stsci.edu:asdf/0.1.0/core/ndarray"

This has the net effect of requiring that the ``data`` property at the
top-level of all ASDF files is tagged as
``tag:stsci.edu:asdf/0.1.0/core/ndarray``.

``propertyOrder`` keyword
^^^^^^^^^^^^^^^^^^^^^^^^^

``propertyOrder``, which applies only to objects, declares that the
object must have its properties presented in the given order.

TBD: It is not yet clear whether this keyword is necessary or desirable.

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

.. _designing-schema:

Designing a new tag and schema
------------------------------

The schema included in the ASDF standard will not be adequate for all
needs, but it is possible to mix them with custom schema designed for
a specific purpose.  It is also possible to extend and specialize an
existing schema (described in :ref:`extending-a-schema`).

This section will walk through the development of a new tag and
schema.  In the example, suppose we work at the institution "SCIENCE"
which can be found on the world wide web at ``science.edu``.  We're
developing a new instrument, ``FOO``, and we need a way to define the
specialized metadata to describe the exposures that it will be
generating.

Header
^^^^^^

Every ASDF schema should begin with the following header::

  %YAML 1.1
  ---
  $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"

This declares that the file is ``YAML 1.1`` format, and that the
structure of the content conforms to ``YAML Schema`` defined above.

Tags and IDs
^^^^^^^^^^^^

All of the tags defined by the ASDF standard itself have the following
prefix::

  tag:stsci.edu:asdf/0.1.0

This prefix is reserved for tags and schemas defined within the ASDF
standard itself.  ASDF can, of course, include any tags, as long as
the tag names are globally unique.  So, for our example instrument,
we'll declare the tag to be::

  tag:science.edu:FOO/0.1.0/metadata

Each tag should be associated with a schema in order to validate
it. Each schema must also have a universally unique ``id``, which is
in the form of unique URI.  For the ASDF built-in tags, the mapping
from tag name to schema URI is quite simple::

  tag:stsci.edu:XXX

maps to::

  http://stsci.edu/schemas/XXX

Note that this URI doesn't actually have to resolve to anything.  In
fact, visiting that URL in your web browser is likely to bring up a
``404`` error.  All that's necessary is that it is universally unique
and that the tool reading the ASDF file is able to map from a tag name
to a schema URI, and then load the associated schema.

Again following with our example, we will assign the following URI to
refer to our schema::

  http://science.edu/schemas/FOO/0.1.0/metadata

Therefore, in our schema file, we have the following keys, one
declaring the name of the YAML ``tag``, and one defining the ``id`` of
the schema::

  tag: "tag:science.edu:FOO/0.1.0/metadata"
  id: "http://science.edu/schemas/FOO/0.1.0/metadata"

Descriptive information
^^^^^^^^^^^^^^^^^^^^^^^

Each schema has some descriptive fields: ``title``, ``description``
and ``examples``.

- ``title``: A one-line summary of what the schema is for.

- ``description``: A lengthier prose description of the schema

- ``examples``: A list of example content that conforms to the schema,
  illustrating how to use it.

Continuing our example::

  title: |
    Metadata for the FOO instrument.
  description: |
    This stores some information about an exposure from the FOO instrument.
  examples:
    -
      - A minimal description of an exposure.
      - |
          !FOO/0.1.0/metadata
            exposure_time: 0.001

The schema proper
^^^^^^^^^^^^^^^^^

The rest of the schema describes the acceptable data types and their
structure.  The format used for this description comes straight out of
JSON Schema, and rather than documenting all of the things it can do
here, please refer to `Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__, and
the further resources available at `json-schema.org
<http://json-schema.org>`__.

In our example, we'll define two metadata elements: the name of the
investigator, and the exposure time, each of which also have a
description::

  type: object
  properties:
    investigator:
      type: string
      description: |
        The name of the principal investigator who requested the
        exposure.

    exposure_time:
      type: number
      description: |
        The time of the exposure, in nanoseconds.

We'll also define an optional element for the exposure time unit.
This is a somewhat contrived example to demonstrate how to include
elements in your schema that are based on the custom types defined in
the ASDF standard::

    exposure_time_units:
      $ref: "http://stsci.edu/schemas/asdf/0.1.0/unit/unit"
      description: |
        The unit of the exposure time.
      default:
        s

Lastly, we'll declare ``exposure_time`` as being required, and allow
extra elements to be added::

  requiredProperties: [exposure_time]
  additionalProperties: true

The complete example
^^^^^^^^^^^^^^^^^^^^

Here is our complete schema example::

  %YAML 1.1
  ---
  $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
  tag: "tag:science.edu:FOO/0.1.0/metadata"
  id: "http://science.edu/schemas/FOO/0.1.0/metadata"

  title: |
    Metadata for the FOO instrument.
  description: |
    This stores some information about an exposure from the FOO instrument.
  examples:
    -
      - A minimal description of an exposure.
      - |
          !FOO/0.1.0/metadata
            exposure_time: 0.001

  type: object
  properties:
    investigator:
      type: string
      description: |
        The name of the principal investigator who requested the
        exposure.

    exposure_time:
      type: number
      description: |
        The time of the exposure, in nanoseconds.

    exposure_time_units:
      $ref: "http://stsci.edu/schemas/asdf/0.1.0/unit/unit"
      description: |
        The unit of the exposure time.
      default:
        s

  requiredProperties: [exposure_time]
  additionalProperties: true

.. _extending-a-schema:

Extending an existing schema
----------------------------

TODO
