.. _extending-asdf:

Schema Design and Editing
=========================
 
.. _designing-new-schema:

Designing a new tag and schema
------------------------------

This section will walk through the development of a new tag and schema. In the
example, suppose we work at the Example Organization, which can be
found on the world wide web at ``example.org``.  We're developing a new
instrument, ``foo``, and we need a way to define the specialized metadata to
describe the exposures that it will be generating.

According to the `naming-conventions`, our ``tag`` and ``id`` attributes will
consist of the following components:

* **organization**: ``example.org``
* **standard**: ``foo``
* **name**: ``metadata``
* **version**: ``1.0.0`` (by convention the starting version for all new schemas)

So, for our example instrument metadata, the tag is::

  tag:example.org:foo/metadata-1.0.0

Each tag should be associated with a schema in order to validate it. Each
schema must also have a universally unique ``id``, which is in the form of
unique URI.

Note that this URI doesn't actually have to resolve to anything.  In fact,
visiting that URL in your web browser is likely to bring up a ``404`` error.
All that's necessary is that it is universally unique and that the tool reading
the ASDF file is able to map from a tag name to a schema URI, and then load the
associated schema.

Again following with our example, we will assign the following URI to refer to
our schema::

  http://example.org/schemas/foo/metadata-1.0.0

Therefore, in our schema file, we have the following keys, one declaring the
name of the YAML ``tag``, and one defining the ``id`` of the schema::

  id: "http://example.org/schemas/foo/metadata-1.0.0"
  tag: "tag:example.org:foo/metadata-1.0.0"


Since our schema is just a basic ASDF schema, we will declare that it conforms
to `yaml-schema` defined by the ASDF Standard::

   $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"

Descriptive information
^^^^^^^^^^^^^^^^^^^^^^^

Continuing our example, we include some `descriptive metadata
<descriptive-info>` about the data type declared by the schema itself::

  title: |
    Metadata for the foo instrument.
  description: |
    This stores some information about an exposure from the foo instrument.
  examples:
    -
      - A minimal description of an exposure.
      - |
          tag:example.org:foo/metadata-1.0.0
            exposure_time: 0.001

The schema proper
^^^^^^^^^^^^^^^^^

The rest of the schema describes the acceptable data types and their structure.
The format used for this description comes straight out of JSON Schema, and
rather than documenting all of the things it can do here, please refer to
`Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__, and the
further resources available at `json-schema.org <http://json-schema.org>`__.

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
  id: "http://example.org/schemas/foo/metadata-1.0.0"
  tag: "tag:example.org:foo/metadata-1.0.0"

  title: |
    Metadata for the foo instrument.
  description: |
    This stores some information about an exposure from the foo instrument.
  examples:
    -
      - A minimal description of an exposure.
      - |
          tag:example.org:foo/metadata-1.0.0
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

Extending an Existing Schema
----------------------------

`JSON Schema`_ does not support the concept of inheritance, which makes it
somewhat awkward to express type hierarchies. However, it is possible to create
a custom schema that adds attributes to an existing schema (e.g. one defined in
the ASDF Standard). It is important to remember that it is not possible to
override or remove any of the attributes from the existing schema.

The following important caveats apply when extending an existing schema:

* It is not possible to redefine, override, or delete any attributes in the
  original schema.
* It will not be possible to add attributes to any node where the original
  schema declares ``additionalProperties: false``
* Instances of the custom type will not be recognized as an instance of the
  original type when resolving schema references or processing YAML tags (i.e.
  there is no concept of polymorphism).

Here's an example of extending a schema using the `software <core/software-1.0.0>`
schema defined by the ASDF Standard.  Here's the original schema, for reference::

  %YAML 1.1
  ---
  $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
  id: "http://stsci.edu/schemas/asdf/core/software-1.0.0"
  title: |
    Describes a software package.
  description: |
    General-purpose description of a software package.

  tag: "tag:stsci.edu:asdf/core/software-1.0.0"
  type: object
  properties:
    name:
      description: |
        The name of the application or library.
      type: string

    author:
      description: |
        The author (or institution) that produced the software package.
      type: string

    homepage:
      description: |
        A URI to the homepage of the software.
      type: string
      format: uri

    version:
      description: |
        The version of the software used.  It is recommended, but not
        required, that this follows the (Semantic Versioning
        Specification)[http://semver.org/spec/v2.0.0.html].
      type: string

  required: [name, version]
  additionalProperties: true
  ...

Since the software schema permits additional properties, we are free
to extend it to include an email address for contacting the author::

  %YAML 1.1
  ---
  $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
  id: "http://somewhere.org/schemas/software_extended-1.0.0"
  title: |
    Describes a software package.
  description: |
    Extension of ASDF core software schema to include the
    software author's contact email.

  allOf:
    - $ref: http://stsci.edu/schemas/asdf/core/software-1.0.0
    - properties:
        author_email:
          description: |
            The contact email of the software author.
          type: string
      required: [author_email]
  ...

The crucial portion of this schema definition is the way that the ``allOf``
operator is used to join a reference to the base software schema with the
definition of a new property called ``author_email``.

The ``allOf`` combiner means that any instance that is validated against
``software_extended-1.0.0`` will have to conform to both the base software schema
and the properties specific to the extended schema.

.. Links

.. _JSON Schema: http://json-schema.org