.. _tree-in-depth:

The tree in-depth
=================

The FINF tree, being encoded in YAML, is built out of the basic
structures common to most dynamic languages: mappings (dict),
sequences (list), and scalars (str, int, float, bool, etc.).  All of
this comes "for free" by using `YAML <http://yaml.org/spec/1.1/>`__.

.. note::

    TODO: The YAML specification is not duplicated here, but long
    term, we probably want to excerpt the important bits here.

.. note::

    **Point for discussion**: OrderedMappings are supported by YAML,
    and could be used to define a canonical ordering of Mapping
    keywords. However, while Python has an OrderedDict that would
    serve well for this purpose, it remains to be seen whether support
    for this concept is good enough in other languages to be relied
    upon, or whether OrderedMappings should remain an optional
    convenience feature of FITS to maintain ordering, but not to
    convey any meaning.

Since these core data structures on their own are so flexible, the
FINF standard includes a number of schema that define the structure of
higher-level content.  For instance, there is a schema that defines
how :ref:`n-dimensional array data
<http://www.stsci.edu/schemas/finf/0.1.0/ndarray>` should be
referenced.  These schema are written in a language called
:ref:`yaml-schema` which is just a thin extension of `JSON Schema,
Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__.  The
chapter, :ref:`schema`, describes all of these schema in detail.

YAML includes the ability to assign :ref:`tags` (or types) to any
object in the tree.  This is an important feature that sets it apart
from other data representation languages, such as JSON.  FINF defines
a number of custom tags, each of which has a corresponding schema.
The tag of the root element of the tree must always be
``tag:stsci.edu:finf/0.1.0/finf``.

.. _tags:

Tags
----

Tags declare the data type of an element in the tree.  A FINF parser
may, for example, use this information for schema validation or use it to
convert to a native data type that presents a nice interface to the
user.

For example::

      %YAML 1.1
      --- !<tag:stsci.edu:finf/0.1.0/finf>
      data: !<tag:stsci.edu:finf/0.1.0/ndarray>
        source: 0
        dtype: float64
        shape: [1024, 1024]
      ...

All tags defined in the FINF standard itself begin with the prefix
``tag:stsci.edu:finf/0.1.0/``.  This can be broken down as:

- ``tag:`` The standard prefix used for all YAML tags.

- ``stsci.edu`` The owner of the tag.

- ``finf`` The name of the standard.

- ``0.1.0`` The version of the standard.

Following that is the tag name itself, for example, ``finf`` or
``ndarray``.  Since it is cumbersome to type out these long prefixes
for every tag, it is recommended to declare a prefix at the top of the
YAML file and use it throughout.  (Most standard YAML writing
libraries have facilities to do this automatically.)  For example, the
following example is equivalent to the above example, but is more
user-friendly.  The ``%TAG`` declaration declares that the exclamation
point (``!``) will be replaced with the prefix
``tag:stsci.edu:finf/0.1.0/``::

      %YAML 1.1
      %TAG ! tag:stsci.edu:finf/0.1.0/
      --- !finf
      data: !ndarray
        source: 0
        dtype: float64
        shape: [1024, 1024]

A FINF parser may use the tag on an element to look up the corresponding
schema in the FINF standard and validate the element.

.. note::

    TODO: Describe how to convert from a tag name to the URL of a schema
    (hint: it's pretty simple.)

A FINF parser may use the tag information to convert the element to a
native data type.  For example, in Python, a FINF parser may convert a
:ref:`ndarray <http://www.stsci.edu/schemas/finf/0.1.0/ndarray>` tag
to a `Numpy <http://www.numpy.org>`__ array, providing a convenient
and familiar interface to the user to access *n*-dimensional data.

The FINF standard does not require parser implementations to validate
or perform native type conversion, however.  A parser may simply leave
the tree represented in the low-level basic data structures.  However,
when writing a FINF file, the elements in the tree must be
appropriately tagged for other tools to make use of them.

FINF parsers must not fail when encountering an unknown tag, but must
simply retain the low-level data structure and the presence of the
tag.  This is important, as end users will likely want to store their
own custom tags in FINF files alongside the tags defined in the FINF
standard itself, and the file must still be readable by FINF parsers
that do not understand those tags.

.. _yaml-schema:

YAML Schema
-----------

YAML Schema is a small extension to `JSON Schema Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__ created
specifically for FINF.
`Understanding JSON Schema
<http://spacetelescope.github.io/understanding-json-schema/>`__
provides a good resource for understanding what it can do.  This
section describes what makes YAML Schema different from JSON Schema,
and provides some examples in the context of FINF.

Writing a new schema is described in :ref:`extending-finf`.

New keywords
^^^^^^^^^^^^

YAML Schema adds two new keywords to JSON Schema.

- ``tag``, which may be attached to any data type, declares that the
  element must have the given YAML tag.  For example, TODO

- ``propertyOrder``, which applies only to objects, declares that the
  object must have its properties presented in the given order.  For
  example, TODO
