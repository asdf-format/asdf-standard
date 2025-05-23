.. _asdf-schemas:

ASDF Schemas
============

ASDF uses `JSON Schema`_ to perform validation of ASDF files. Schema validation
of ASDF files serves the following purposes:

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
Standard also defines other schemas, which are optional for ASDF implementations
and maintained as part of the standard (mainly for historical reasons):

* :ref:`astronomy <astronomy-schema>`

The ASDF Standard also defines two metaschemas which are used to validate the
ASDF schemas themselves:

* :ref:`yaml-schema`
* :ref:`ASDF Schema <asdf-schema-1.1.0>`

More information on the schemas defined by ASDF can be found in :ref:`schema`.

Schema Implementation
---------------------

ASDF schemas are encoded in YAML and conform to a superset of `JSON Schema`_
called :ref:`yaml-schema`. The version of YAML supported by ASDF is 1.1.
Accordingly, all schemas begin with the following YAML header::

  %YAML 1.1
  ---

The following top-level attributes are required for all ASDF schemas:

* ``$schema``: Indicates the metaschema definition used to validate this schema
* ``id``: A name that uniquely identifies the schema

Each of these attributes is described in more detail below.

$schema
^^^^^^^

ASDF schemas use the top-level ``$schema`` attribute to declare the metaschema
that is used to validate the schema itself. Most custom ASDF schemas will
conform to :ref:`YAML Schema <yaml-schema>` defined by the ASDF Standard, and
so will have the following top-level attribute::

   $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"

Some ASDF schemas use the :ref:`ASDF metaschema <asdf-schema-1.1.0>` instead
(e.g. `ndarray <core/ndarray-1.1.0>`).  It is also possible to create custom
metaschemas.

.. warning::

   Creating a new custom metaschema is highly discouraged. Many JSON schema
   libraries do not support custom metaschemas. If creating a custom metaschema it
   should inherit from YAML Schema. [#]_

Some ASDF implementations may choose to validate the schemas themselves (e.g.
as part of a regression testing suite). The ``$schema`` keyword should be used
to determine the metaschema to be used for validation. All schemas should also
validate successfully against :ref:`yaml-schema`.

id
^^

The ``id`` represents the globally unique name of the schema. It must be a
`valid URI <https://tools.ietf.org/html/rfc3986>`__ and cannot be an empty
string or an empty fragment (e.g. ``#``).  See `naming-conventions` for
conventions to ensure global uniqueness.

While the ``id`` must be a valid URI, it does not have to describe a real
location on disk or on a network. For example, the ``id`` values for all
schemas in the ASDF Standard begin with the prefix
``http://stsci.edu/schemas/asdf/``.  However, as of this writing, none of the
schemas are actually hosted at that location.

The ``id`` keyword is used for reference resolution both within a schema and
between schemas. Relative references within a schema are resolved against the
``id`` of that schema. A reference to an external schema uses the ``id`` of
that schema. See `schema-references` below for additional information.

Each ASDF implementation must define how to resolve a schema ``id`` to a real
resource that contains the schema itself. This resource will often be a local
file but this detail is left up to the implementation.

.. _descriptive-info:

Descriptive information
^^^^^^^^^^^^^^^^^^^^^^^

Each schema may optionally contain descriptive fields: ``title``,
``description`` and ``examples``.  These fields may contain core markdown
syntax (which will be used for the purposes of rendering schema documentation
by, for example, `sphinx-asdf
<https://github.com/spacetelescope/sphinx-asdf>`__).

- ``title``: A one-line summary of the data type described by the schema

- ``description``: A lengthier prose description of the schema

- ``examples``: A list of example content that conforms to the schema,
  illustrating how to use it.


.. _schema-references:

References
^^^^^^^^^^

`JSON Schema`_ allows rerencing other schemas by including
a mapping containing a single key ``$ref`` and value containing the ``uri``
of the referenced schema.

.. _naming-conventions:

Naming Conventions
^^^^^^^^^^^^^^^^^^

Schema ``id`` attributes must be valid URIs. Furthermore ``tag`` uris must be
valid URIs that conform to the tag URI scheme defined in `RFC 4151`_.
Certain conventions are **strongly** recommended in order to ensure
uniqueness and to enable a simple correspondence between the ``id`` and ``tag``
attributes. These conventions are described below.

All schema ids should encode the following information:

* **organization**: Indicates the organization that created the schema
* **standard**: The "standard" this schema belongs to. This will usually
  correspond to the name of the software package that provides this schema.
* **name**: The name of the data type corresponding to this schema.
* **version**: The version of the schema. See `versioning-conventions` for more
  details.

Consider the schemas from the ASDF Standard as an example. In this case, the
**organization** is ``stsci.edu``, which is the web address of the organization
that created the schemas. The **standard** is ``asdf``. Each individual schema
in the ASDF Standard has a different **name** field. In the case of the
:ref:`ndarray <core/ndarray-1.1.0>` data type, for example, the name is
``core/ndarray``. The version of `ndarray <core/ndarray-1.1.0>` is ``1.1.0``.
Some other types in the ASDF Standard have multiple versions, such as
``quantity-1.1.0`` and :ref:`quantity-1.2.0 <unit/quantity-1.2.0>`.

While schema ids can be any valid URI, under this convention they always begin
with ``http://``. The general format of the id attribute becomes::

   http://<organization>/schemas/<standard>/<name>-<version>

Continuing with the example of :ref:`ndarray <core/ndarray-1.1.0>`, we have::

   id: "http://stsci.edu/schemas/asdf/core/ndarray-1.1.0"

The idea behind the convention for ``id`` is that it should be possible (in
principle if not in practice) for schemas to be hosted at the corresponding
URL. This motivates the choice of the organization's web address as the
**organization** component. However, this is not a requirement. The primary
objective is to create a globally unique id.

.. _extending-asdf:

Designing a new tag and schema
------------------------------

This section will walk through the development of a new tag and schema. In the
example, suppose we work at the Example Organization, which can be
found on the world wide web at ``example.org``.  We're developing a new
instrument, ``foo``, and we need a way to define the specialized metadata to
describe the exposures that it will be generating.

According to the `naming-conventions`, our ``tag`` and ``id`` will
consist of the following components:

* **organization**: ``example.org``
* **standard**: ``foo``
* **name**: ``metadata``
* **version**: ``1.0.0`` (by convention the starting version for all new schemas)

So, for our example instrument metadata, the tag is::

  tag:example.org:foo/metadata-1.0.0

Each tag should be associated with a schema in order to validate it. Each
schema must also have a universally unique ``id``, which is in the form of
unique URI. We will assign the following URI to refer to our schema::

  http://example.org/schemas/foo/metadata-1.0.0

.. note::

   Note that this URI doesn't actually have to resolve to anything.  In fact,
   visiting that URL in your web browser is likely to bring up a ``404`` error.
   All that's necessary is that it is universally unique and that the tool reading
   the ASDF file is able to map from a tag name to a schema URI, and then load the
   associated schema.

Therefore, in our schema file, we have the following defining the ``id`` of the schema::

  id: "http://example.org/schemas/foo/metadata-1.0.0"


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
the resources available at `json-schema.org <http://json-schema.org>`__.

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
      allOf:
        - $ref: "http://stsci.edu/schemas/asdf/unit/unit-1.0.0"
      description: |
        The unit of the exposure time.

In brief this requires that any value for ``exposure_time_units`` must
comply with the `unit <unit/unit-1.0.0>` schema.

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
      allOf:
        - $ref: "http://stsci.edu/schemas/asdf/unit/unit-1.0.0"
      description: |
        The unit of the exposure time.

  required: [exposure_time]
  additionalProperties: true

.. _extending-a-schema:

Extending an existing schema
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

.. _default-annotation:

Default annotation
------------------

.. warning::

   It is recommended that ``default`` is no longer used  in new schema.
   As noted below newer versions of the standard will ignore these values.


The JSON Schema spec includes a schema annotation attribute called ``default`` that
can be used to describe the default value of a data attribute when that attribute
is missing.  Recent versions of the spec `point out <http://json-schema.org/draft/2019-09/json-schema-core.html#rfc.section.7.7.1.1>`__
that there is no single correct way to choose an annotation value when multiple
are available due to references and combiners.  This presents a problem when
trying to fill in missing data in a file based on the schema ``default``: if
multiple conflicting values are available, the software does not know how to choose.

Previous versions of the ASDF Standard did not offer guidance on how
to use ``default``.  The Python reference implementation read the first default
that it encountered as a literal value and inserted that value into the tree when
the corresponding attribute was otherwise missing.  Until version 2.8, it also
removed attributes on write whose values matched their schema defaults.  The
resulting files would appear to the casual viewer to be missing data, and may in
fact be invalid against their schemas if the any of the removed attributes were required.

Implementations **must not** remove attributes with default values from the tree.
Beginning with ASDF Standard 1.6.0, implementations also must not fill default values
directly from the schema.  This will avoid ambiguity when multiple schema defaults
are present, and also permit the ``default`` attribute to contain a description
that is not appropriate to use as a literal default value.  For example::

    default: An array of zeros matching the dimensions of the data array.

For ASDF Standard < 1.6.0, filling default values from the schema is required.  This is
necessary to support files written by older versions of the Python implementation.

.. rubric:: Footnotes

.. [#] Implementations may expose the control of validation on reading to the
   user (e.g. to disable it on demand). However, validation on reading should
   be the default behavior.
.. [#] For an example of how to inherit from another metaschema, look at the
   :ref:`contents <asdf-schema-1.1.0>`
   of the ASDF metaschema and see how there is a reference to the YAML schema
   in the top-level ``allOf``.

.. Links

.. _JSON Schema: http://json-schema.org
.. _RFC 4151: https://tools.ietf.org/html/rfc4151
