.. _extending-asdf:

ASDF Schemas
============

ASDF uses `JSON Schema <http://json-schema.org/>`__ to perform validation of
ASDF files. Schema validation of ASDF files serves the following purposes:

* Ensures conformity with core data types defined by the ASDF Standard. ASDF
  readers can detect whether an ASDF file has been modified in a way that would
  render it unreadable or unrecognizable.
* Enables interoperability between ASDF implementations. Implementations that
  recognize the same schema definitions should be able to interpret files
  containing instances of data types that conform to those schemas.
* Allows for the definition of custom data types. External software packages
  can provide ASDF schemas that correspond to types provided by that package,
  and then serialize instances of those types in a way that is standardized
  and portable.

All ASDF implementations must implement the types defined by the `core schemas
<core-schema>` and validate against them when reading files. [#]_ The ASDF
Standard also defines several other categories of schemas, which are optional
for ASDF implementations:

* :ref:`unit <unit-schema>`
* :ref:`time <time-schema>`
* :ref:`transform <transform-schema>`
* :ref:`World Coordinate System (WCS) <wcs-schema>` (primarily intended for
  astronomical applications)
* :ref:`FITS <fits-schema>` (not likely to be of general use)

The ASDF Standard also defines two metaschemas which are used to validate the
ASDF schemas themselves:

* :ref:`yaml-schema`
* :ref:`ASDF Schema <asdf-schema-1.0.0>`

More information on the schemas defined by ASDF can be found in :ref:`schema`.

.. _designing-schema:

Designing a new tag and schema
------------------------------

This section will walk through the development of a new tag and schema. In the
example, suppose we work at the Space Telescope Science Institute, which can be
found on the world wide web at ``stsci.edu``.  We're developing a new
instrument, ``FOO``, and we need a way to define the specialized metadata to
describe the exposures that it will be generating.

YAML Header
^^^^^^^^^^^

ASDF schemas are encoded in YAML. The version of YAML currently used by ASDF is
1.1. Therefore all ASDF schemas begin with the following YAML header::

  %YAML 1.1
  ---

Metaschema
^^^^^^^^^^

ASDF schemas use the top-level ``$schema`` attribute to declare the metaschema
that is used to validate the schema itself. Most custom ASDF schemas will
conform to :ref:`YAML Schema <yaml-schema>` defined by the ASDF Standard, and
so will have the following::

   $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"

Some ASDF schemas use the :ref:`ASDF metaschema <asdf-schema-1.0.0>` instead
(e.g. `core/ndarray-1.0.0`).  It is also possible to create custom metaschemas,
although these should always inherit from either YAML Schema or the ASDF
metaschema. [#]_

Tags and IDs
^^^^^^^^^^^^

Each schema should contain two top-level properties: ``id`` and ``tag``. This
requirement is currently not enforced by the YAML Schema but may be in a future
version of the ASDF Standard. Creators of new schemas should assume that both
fields are required.

``id`` keyword
""""""""""""""

The ``id`` represents the name of the schema. It must be a valid URI and cannot
be an empty string or an empty fragment (e.g. ``#``).

The ``id`` keyword is used for reference resolution both within a schema and
between schemas. Relative references within a schema are resolved against the
``id`` of that schema. A reference to an external schema uses the ``id`` of
that schema.

While the ``id`` must be a valid URI, it does not have to describe a real
location on disk or on a network. For example, the ``id`` value for all schemas
in the ASDF Standard begin with the prefix ``http://stsci.edu/schemas/asdf/``.
However, as of this writing, none of the schemas are actually hosted at that
location. The primary requirement of the ``id`` is that it be a unique
identifier; it should not be possible for the ``id`` values of any two
different schemas to collide.

Each ASDF implementation must define how to resolve a schema ``id`` to a real
resource that contains the schema itself. This could be done in a variety of
ways, but the following seem like the most likely possibilities:

* Resolve the ``id`` to a real network location (assuming the schema is
  actually hosted at that location)
* Map the ``id`` to a file location on disk that contains the schema

Other mappings are possible in theory. For example, a schema could be stored
in a string literal as part of a program.

``tag`` keyword
"""""""""""""""

All of the tags defined by the ASDF standard itself have the following
prefix::

  tag:stsci.edu:asdf/

This prefix is reserved for tags and schemas defined within the ASDF
standard itself.  ASDF can, of course, include any tags, as long as
the tag names are globally unique.  So, for our example instrument,
we'll declare the tag to be::

  tag:stsci.edu:FOO/metadata-1.0.0

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

  http://stsci.edu/schemas/FOO/metadata-1.0.0

Therefore, in our schema file, we have the following keys, one
declaring the name of the YAML ``tag``, and one defining the ``id`` of
the schema::

  tag: "tag:stsci.edu:FOO/metadata-1.0.0"
  id: "http://stsci.edu/schemas/FOO/metadata-1.0.0"

Descriptive information
^^^^^^^^^^^^^^^^^^^^^^^

Each schema has some descriptive fields: ``title``, ``description``
and ``examples``.  These fields may contain core markdown syntax.

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
          !FOO/metadata-1.0.0
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
      $ref: "http://stsci.edu/schemas/asdf/unit/unit-1.0.0"
      description: |
        The unit of the exposure time.
      default:
        s

Lastly, we'll declare ``exposure_time`` as being required, and allow
extra elements to be added::

  required: [exposure_time]
  additionalProperties: true

The complete example
^^^^^^^^^^^^^^^^^^^^

Here is our complete schema example::

  %YAML 1.1
  ---
  $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
  tag: "tag:stsci.edu:FOO/metadata-1.0.0"
  id: "http://stsci.edu/schemas/FOO/metadata-1.0.0"

  title: |
    Metadata for the FOO instrument.
  description: |
    This stores some information about an exposure from the FOO instrument.
  examples:
    -
      - A minimal description of an exposure.
      - |
          !FOO/metadata-1.0.0
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
      $ref: "http://stsci.edu/schemas/asdf/unit/unit-1.0.0"
      description: |
        The unit of the exposure time.
      default:
        s

  required: [exposure_time]
  additionalProperties: true

.. _extending-a-schema:

Extending an existing schema
----------------------------

TODO

.. rubric:: Footnotes

.. [#] Implementations may expose the control of validation on reading to the
   user (e.g. to disable it on demand). However, validation on reading should
   be the default behavior.
.. [#] For an example of how to inherit from another metaschema, look at the
   `contents
   <generated/stsci.edu/asdf/asdf-schema-1.0.0.html#Original%20Schema>`__
   of the ASDF metaschema and see how there is a reference to the YAML schema
   in the top-level ``allOf``.
