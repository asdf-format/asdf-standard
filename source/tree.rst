.. _tree-in-depth:

The tree in-depth
=================

The ASDF tree, being encoded in YAML, is built out of the basic
structures common to most dynamic languages: mappings (dictionaries),
sequences (lists), and scalars (strings, integers, floating-point
numbers, booleans, etc.).  All of this comes "for free" by using `YAML
<http://yaml.org/spec/1.1/>`__.

Since these core data structures on their own are so flexible, the
ASDF standard includes a number of schema that define the structure of
higher-level content.  For instance, there is a schema that defines
how :ref:`n-dimensional array data
<http://www.stsci.edu/schemas/asdf/0.1.0/core/ndarray>` should be
described.  These schema are written in a language called
:ref:`yaml-schema` which is just a thin extension of `JSON Schema,
Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__.
:ref:`schema`, provides a reference to all of these schema in detail.
:ref:`extending-asdf` describes how to use YAML schema to define new
schema.

.. _tags:

Tags
----

YAML includes the ability to assign :ref:`tags` (or types) to any
object in the tree.  This is an important feature that sets it apart
from other data representation languages, such as JSON.  ASDF defines
a number of custom tags, each of which has a corresponding schema.
For example the tag of the root element of the tree must always be
``tag:stsci.edu:asdf/0.1.0/core/asdf``, which corresponds to the
:ref:`asdf schema <http://www.stsci.edu/schemas/asdf/0.1.0/core/asdf>`
schema.  A validating ASDF reader would encounter the tag when reading
in the file, load the corresponding schema, and validate the content
against it.  An ASDF library may also use this information to convert
to a native data type that presents a more convenient interface to the
user than the structure of basic types stored in the YAML content.

For example::

     %YAML 1.1
     --- !<tag:stsci.edu:asdf/0.1.0/core/asdf>
     data: !<tag:stsci.edu:asdf/0.1.0/core/ndarray>
       source: 0
       dtype: float64
       shape: [1024, 1024]
     ...

All tags defined in the ASDF standard itself begin with the prefix
``tag:stsci.edu:asdf/0.1.0/``.  This can be broken down as:

- ``tag:`` The standard prefix used for all YAML tags.

- ``stsci.edu`` The owner of the tag.

- ``asdf`` The name of the standard.

- ``0.1.0`` The version of the standard.

Following that is the "module" containing the schema (see
:ref:`schema` for a list of the available modules).  Lastly is the tag
name itself, for example, ``asdf`` or ``ndarray``.  Since it is
cumbersome to type out these long prefixes for every tag, it is
recommended that ASDF files declare a prefix at the top of the YAML
file and use it throughout.  (Most standard YAML writing libraries
have facilities to do this automatically.)  For example, the following
example is equivalent to the above example, but is more user-friendly.
The ``%TAG`` declaration declares that the exclamation point (``!``)
will be replaced with the prefix ``tag:stsci.edu:asdf/0.1.0/``::

      %YAML 1.1
      %TAG ! tag:stsci.edu:asdf/0.1.0/
      --- !core/asdf
      data: !core/ndarray
        source: 0
        dtype: float64
        shape: [1024, 1024]

An ASDF parser may use the tag to look up the corresponding schema in
the ASDF standard and validate the element.  The schema definitions
ship as part of the ASDF standard.

An ASDF parser may also use the tag information to convert the element
to a native data type.  For example, in Python, an ASDF parser may
convert a :ref:`ndarray
<http://www.stsci.edu/schemas/asdf/0.1.0/core/ndarray>` tag to a
`Numpy <http://www.numpy.org>`__ array instance, providing a
convenient and familiar interface to the user to access
*n*-dimensional data.

The ASDF standard does not require parser implementations to validate
or perform native type conversion, however.  A parser may simply leave
the tree represented in the low-level basic data structures.  When
writing an ASDF file, however, the elements in the tree must be
appropriately tagged for other tools to make use of them.

ASDF parsers must not fail when encountering an unknown tag, but must
simply retain the low-level data structure and the presence of the
tag.  This is important, as end users will likely want to store their
own custom tags in ASDF files alongside the tags defined in the ASDF
standard itself, and the file must still be readable by ASDF parsers
that do not understand those tags.

.. _references:

References
----------

It is possible to directly reference other items within the same tree
or within the tree of another ASDF file.  This functionality is based
on two IETF standards: `JSON Pointer (IETF RFC 6901)
<http://tools.ietf.org/html/rfc6901>`__ and `JSON Reference (Draft 3)
<http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03>`__.

A reference is represented as a mapping (dictionary) with a single
key/value pair. The key is always the special keyword ``$ref`` and the
value is a URI.  The URI may contain a fragment (the part following
the ``#`` character) in JSON Pointer syntax that references a specific
element within the external file.  This is a ``/``-delimited path
where each element is a mapping key or an array index.  If no fragment
is present, the reference refers to the top of the tree.

.. note::

   JSON Pointer is a very simple convention.  The only wrinkle is that
   because the characters ``'~'`` (x7E) and ``'/'`` (%x2F) have
   special meanings, ``'~'`` needs to be encoded as ``'~0'`` and
   ``'/'`` needs to be encoded as ``'~1'`` when these characters
   appear in a reference token.

When these references are resolved, this mapping should be treated as
having the same logical content as the target of the URI, though the
exact details of how this is performed is dependent on the
implementation, i.e., a library may copy the target data into the
source tree, or it may insert a proxy object that is lazily loaded at
a later time.

For example, suppose we had a given ASDF file containing some shared
reference data, available on a public webserver at the URI
``http://www.nowhere.com/reference.asdf``::

    wavelengths:
      - !ndarray
        source: 0
        shape: [256, 256]
        dtype: float

Another file may reference this data directly::

    reference_data:
      $ref: "http://www.nowhere.com/reference.asdf#wavelengths/0"

It is also possible to use references within the same file::

    data: !ndarray
      source: 0
      shape: [256, 256]
      dtype: float
      mask:
        $ref: "#/my_mask"

    my_mask: !ndarray
      source: 0
      shape: [256, 256]
      dtype: uint8

Reference resolution should be performed *after* the entire tree is
read, therefore forward references within the same file are explicitly
allowed.

.. note::
    The YAML 1.1 standard itself also provides a method for internal
    references called "anchors" and "aliases".  It does not, however,
    support external references.  While ASDF does not explicitly
    disallow YAML anchors and aliases, since it explicitly supports
    all of YAML 1.1, their use is discouraged in favor of the more
    flexible JSON Pointer/JSON Reference standard described above.
