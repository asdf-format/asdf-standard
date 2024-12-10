.. _asdf-schemas:

ASDF Schemas
============

.. toctree::
   :maxdepth: 2
   :hidden:

   Schema Definitions <definitions.rst>
   Meta Schemas <meta-schemas.rst>
   Manifests <manifest.rst>
   Schema Implementation <implementation.rst>
   Schema Design and Editing <extending-asdf.rst>
   Default Annotation <default-annotation.rst>


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
<core-schema>` and validate against them when reading files. [#]_

.. note::
  .. [#]

  Implementations may expose the control of validation on reading to the
  user (e.g. to disable it on demand). However, validation on reading should
  be the default behavior.


The ASDF
Standard also defines other schemas, which are optional for ASDF implementations
and maintained as part of the standard (mainly for historical reasons):

* :ref:`astronomy <astronomy-schema>`

More information on the schemas defined by ASDF can be found in :ref:`schema`.

The ASDF Standard also defines two metaschemas which are used to validate the
ASDF schemas themselves:

* :doc:`YAML schema <yaml_schema>`
* :doc:`ASDF Schema <asdf>`

The ASDF tags (described by schemas) available under each ASDF standard version are all described
by a single :doc:`manifest <manifest>` document for that ASDF standard version.


.. Links

.. _JSON Schema: http://json-schema.org
