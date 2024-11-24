.. _implementation:

Schema Implementation
---------------------

ASDF schemas are encoded in YAML and conform to a superset of `JSON Schema`_
called :doc:`yaml_schema`. The version of YAML supported by ASDF is 1.1.
Accordingly, all schemas begin with the following YAML header::

  %YAML 1.1
  ---

The following top-level attributes are required for all ASDF schemas: [#]_

* ``$schema``: Indicates the metaschema definition used to validate this schema
* ``id``: A name that uniquely identifies the schema
* ``tag``: The YAML tag corresponding to the type described by this schema

Each of these attributes is described in more detail below.

$schema
^^^^^^^

ASDF schemas use the top-level ``$schema`` attribute to declare the metaschema
that is used to validate the schema itself. Most custom ASDF schemas will
conform to :doc:`YAML Schema <yaml_schema>` defined by the ASDF Standard, and
so will have the following top-level attribute::

   $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"

Some ASDF schemas use the :ref:`ASDF metaschema <asdf-schema-1.1.0>` instead
(e.g. `ndarray <core/ndarray-1.0.0>`).  It is also possible to create custom
metaschemas, although these should always inherit from either `YAML Schema <yaml_schema>` or
the `ASDF metaschema <asdf>`. [#]_

Some ASDF implementations may choose to validate the schemas themselves (e.g.
as part of a regression testing suite). The ``$schema`` keyword should be used
to determine the metaschema to be used for validation. All schemas should also
validate successfully against :ref:`yaml_schema`.

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
resource that contains the schema itself. This could be done in a variety of
ways, but the following seem like the most likely possibilities:

* Resolve the ``id`` to a real network location (assuming the schema is
  actually hosted at that location)
* Map the ``id`` to a file location on disk that contains the schema

Other mappings are possible in theory. For example, a schema could be stored
in a string literal as part of a program.

tag
^^^

The ``tag`` attribute is used by ASDF to associate an instance of a data type
in an ASDF file with the appropriate schema to be used for validation. It is a
concept from YAML (see the `documentation
<https://yaml.org/spec/1.1/#tag/information%20model>`__).

Libraries that provide custom schemas must ensure that the YAML tag that is
written for a particular data type must match the ``tag`` attribute in the
schema that corresponds to the data type. Tags must conform to the tag URI
scheme which is defined in `RFC 4151`_, but are otherwise perfectly arbitrary.
However, certain `naming-conventions` are recommended in order to facilitate a
mapping between ``tag`` and ``id`` attributes.

ASDF implementations must be able to map ``tag`` attributes to the
corresponding schema ``id``. The way that this mapping is defined is up to
individual implementations. However, if the `naming-conventions` are followed,
most implementations will be able to perform prefix matching and replacement.

While the ``id`` attribute will almost certainly become required in a future
version of the ASDF Standard, the ``tag`` attribute may remain optional. This
is because schemas can be referenced by ``id`` without necessarily referring to
a particular tagged type in the YAML representation.

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

A particular ASDF schema can contain references to other ASDF schemas.
References are encoded by using the ``$ref`` attribute anywhere in the tree.
While `JSON Schema`_ references are purely based on ``id``, ASDF
implementations must be able to resolve references using both ``id`` and
``tag`` attributes.

The resolution of ``id`` or ``tag`` references to actual schema files is up to
individual implementations. It is recommended for ASDF implementations to
use a two-phase mapping: one from ``tag`` to ``id``, and another from ``id`` to
an actual schema resource. In most cases, the ``id`` will be resolved to a
location on disk (e.g. to a schema file that is installed in a known location).
However, other scenarios might involve schemas that are hosted on a network, or
schemas that are embedded in source files as string literals.

.. _naming-conventions:

Naming Conventions
^^^^^^^^^^^^^^^^^^

Schema ``id`` attributes must be valid URIs. Schema ``tag`` attributes must be
valid URIs that conform to the tag URI scheme defined in `RFC 4151`_ Aside from
these requirements, assignment of these attributes is perfectly arbitrary.
However, certain conventions are **strongly** recommended in order to ensure
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
:ref:`ndarray <core/ndarray-1.0.0>` data type, for example, the name is
``core/ndarray``. The version of `ndarray <core/ndarray-1.0.0>` is ``1.0.0``.
Some other types in the ASDF Standard have multiple versions, such as
``quantity-1.0.0`` and :ref:`quantity-1.1.0 <unit/quantity-1.1.0>`.

While schema ids can be any valid URI, under this convention they always begin
with ``http://``. The general format of the id attribute becomes::

   http://<organization>/schemas/<standard>/<name>-<version>

Continuing with the example of :ref:`ndarray <core/ndarray-1.0.0>`, we have::

   id: "http://stsci.edu/schemas/asdf/core/ndarray-1.0.0"

The idea behind the convention for ``id`` is that it should be possible (in
principle if not in practice) for schemas to be hosted at the corresponding
URL. This motivates the choice of the organization's web address as the
**organization** component. However, this is not a requirement. The primary
objective is to create a globally unique id.

Given the components defined above, the ``tag`` definition follows in a
straightforward manner. The generic tag URI template is::

   tag:<organization>:<standard>/<name>-<version>

Considering `ndarray <core/ndarray-1.0.0>` once again, we have::

   tag: "tag:stsci.edu:asdf/core/ndarray-1.0.0"

Following the naming convention for both ``id`` and ``tag`` attributes enables
a simple mapping from ``tag`` to ``id``. In this case, simply take the prefix
``tag:stsci.edu:`` and replace it with ``http://stsci.edu/schemas/``.



.. rubric:: Footnotes

.. [#] The presence of ``id`` and ``tag`` is not currently enforced by the YAML
   Schema but may be in a future version of the ASDF Standard. Authors of new
   schemas should assume that at the very least ``id`` will be required in a
   future version of the Standard.
.. [#] For an example of how to inherit from another metaschema, look at the
   `contents
   <generated/stsci.edu/asdf/asdf-schema-1.0.0.html#Original%20Schema>`__
   of the ASDF metaschema and see how there is a reference to the YAML schema
   in the top-level ``allOf``.


.. Links

.. _JSON Schema: http://json-schema.org
.. _RFC 4151: https://tools.ietf.org/html/rfc4151