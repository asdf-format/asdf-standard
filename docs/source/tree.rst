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
how :ref:`n-dimensional array data <core/ndarray-1.0.0>` should be
described.  These schema are written in a language called
:ref:`yaml-schema` which is just a thin extension of `JSON Schema,
Draft 4
<http://json-schema.org/latest/json-schema-validation.html>`__.  (Such
extensions are allowed and even encouraged by the JSON Schema
standard, which defines the ``$schema`` attribute as a place to
specify which extension is being used.) `asdf-schemas` contains an overview of
how schemas are defined and used by ASDF. :ref:`schema` describes in detail
all of the schemas provided by the ASDF Standard.  reference to all of schemas
in detail.

.. _yaml_subset:

YAML subset
-----------

For reasons of portability, some features of YAML 1.1 are not
permitted in an ASDF tree.

Restricted mapping keys
^^^^^^^^^^^^^^^^^^^^^^^

YAML itself places no restrictions on the object type used as a mapping key;
floats, sequences, even mappings themselves can serve as a key.  For example,
the following is a perfectly valid YAML document::

      %YAML 1.1
      ---
      {foo: bar}:
        3.14159: baz
        [1, 2, 3]: qux
      ...

However, such a file may not be easily parsed in all languages.  Python,
for example, does not include a hashable mapping type, so the two major
Python YAML libraries both fail to construct the object described by this
document.  Floating-point keys are described as "not recommended" in the
YAML 1.1 spec because YAML does not specify an accuracy for floats.

For these reasons, mapping keys in ASDF trees are restricted to
the following scalar types:

- bool
- int
- str

.. _tags:

Tags
----

YAML includes the ability to assign :ref:`tags` (or types) to any
object in the tree.  This is an important feature that sets it apart
from other data representation languages, such as JSON.  ASDF defines
a number of custom tags, each of which has a corresponding schema.
For example the tag of the root element of the tree must always be
``tag:stsci.edu:asdf/core/asdf-1.1.0``, which corresponds to the
:ref:`asdf schema <core/asdf-1.1.0>` --in other words, the top level schema for
ASDF trees.  A validating ASDF reader would encounter the tag when reading in
the file, load the corresponding schema, and validate the content against it.
An ASDF library may also use this information to convert to a native data type
that presents a more convenient interface to the user than the structure of
basic types stored in the YAML content.

For example::

     %YAML 1.1
     --- !<tag:stsci.edu:asdf/core/asdf-1.1.0>
     data: !<tag:stsci.edu:asdf/core/ndarray-1.0.0>
       source: 0
       datatype: float64
       shape: [1024, 1024]
       byteorder: little
     ...

All tags defined in the ASDF standard itself begin with the prefix
``tag:stsci.edu:asdf/``.  This can be broken down as:

- ``tag:`` The standard prefix used for all YAML tags.

- ``stsci.edu`` The owner of the tag.

- ``asdf`` The name of the standard.

Following that is the "module" containing the schema (see
:ref:`schema` for a list of the available modules).  Lastly is the tag
name itself, for example, ``asdf`` or ``ndarray``.  Since it is
cumbersome to type out these long prefixes for every tag, it is
recommended that ASDF files declare a prefix at the top of the YAML
file and use it throughout.  (Most standard YAML writing libraries
have facilities to do this automatically.)  For example, the following
example is equivalent to the above example, but is more user-friendly.
The ``%TAG`` declaration declares that the exclamation point (``!``)
will be replaced with the prefix ``tag:stsci.edu:asdf/``::

      %YAML 1.1
      %TAG ! tag:stsci.edu:asdf/
      --- !core/asdf-1.1.0
      data: !core/ndarray-1.0.0
        source: 0
        datatype: float64
        shape: [1024, 1024]
        byteorder: little

An ASDF parser may use the tag to look up the corresponding schema in
the ASDF standard and validate the element.  The schema definitions
ship as part of the ASDF standard.

An ASDF parser may also use the tag information to convert the element
to a native data type.  For example, in Python, an ASDF parser may
convert a :ref:`ndarray <core/ndarray-1.0.0>` tag to a `Numpy
<http://www.numpy.org>`__ array instance, providing a convenient and familiar
interface to the user to access *n*-dimensional data.

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
   because the characters ``'~'`` (0x7E) and ``'/'`` (0x2F) have
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
      - !core/ndarray
        source: 0
        shape: [256, 256]
        datatype: float
        byteorder: little

Another file may reference this data directly::

    reference_data:
      $ref: "http://www.nowhere.com/reference.asdf#/wavelengths/0"

It is also possible to use references within the same file::

    data: !core/ndarray
      source: 0
      shape: [256, 256]
      datatype: float
      byteorder: little
      mask:
        $ref: "#/my_mask"

    my_mask: !core/ndarray
      source: 0
      shape: [256, 256]
      datatype: uint8
      byteorder: little

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

.. _numeric-literals:

Numeric literals
----------------

Integers represented as string literals in the ASDF tree must be no more than
64-bits.  Due to ``ndarray`` types in
:ref:`Numpy <numpy:numpy_docs_mainpage>`, this is further restricted to
ranges defined for signed 64-bit integers (int64), not unsigned 64-bit integers
(uint64).

.. _tree-comments:

Comments
--------

It is quite common in FITS files to see comments that describe the
purpose of the key/value pair.  For example::

  DATE    = '2015-02-12T23:08:51.191614' / Date this file was created (UTC)
  TACID   = 'NOAO    '           / Time granting institution

Bringing this convention over to ASDF, one could imagine::

  # Date this file was created (UTC)
  creation_date: !time/utc
    2015-02-12T23:08:51.191614
  # Time granting institution
  time_granting_institution: NOAO

It should be obvious from the examples that these kinds of comments,
describing the global meaning of a key, are much less necessary in
ASDF.  Since ASDF is not limited to 8-character keywords, the keywords
themselves can be much more descriptive.  But more importantly, the
schema for a given key/value pair describes its purpose in detail.
(It would be quite straightforward to build a tool that, given an
entry in a YAML tree, looks up the schema's description associated
with that entry.)  Therefore, the use of comments to describe the
global meaning of a value are strongly discouraged.

However, there still may be cases where a comment may be desired in
ASDF, such as when a particular value is unusual or unexpected.  The
YAML standard includes a convention for comments, providing a handy
way to include annotations in the ASDF file::

  # We set this to filter B here, even though C is the more obvious
  # choice, because B is handled with more accuracy by our software.
  filter:
    type: B

Unfortunately, most YAML parsers will simply throw these comments out
and do not provide any mechanism to retain them, so reading in an ASDF
file, making some changes, and writing it out will remove all
comments.  Even if the YAML parser could be improved or extended to
retain comments, the YAML standard does not define which values the
comments are associated with.  In the above example, it is only by
standard reading conventions that we assume the comment is associated
with the content following it.  If we were to move the content, where
should the comment go?

To provide a mechanism to add user comments without swimming upstream
against the YAML standard, we recommend a convention for associating
comments with objects (mappings) by using the reserved key name
``//``.  In this case, the above example would be rewritten as::

  filter:
    //: |
      We set this to filter B here, even though C was used, because B
      is handled with more accuracy by our software.
    type: B

ASDF parsers must not interpret or react programmatically to these
comment values: they are for human reference only.  No schema may
use ``//`` as a meaningful key.


Null values
-----------

YAML permits serialization of null values using the ``null`` literal::

    some_key: null

Previous versions of the ASDF Standard were vague as to how nulls should
be handled, and the Python reference implementation did not distinguish
between keys with null values and keys that were missing altogether (and
in fact, removed any keys assigned ``None`` from the tree on read or
write).  Beginning with ASDF Standard 1.6.0, ASDF implementatations
are required to preserve keys even if assigned null values.  This
requirement does not extend back into previous versions, and users
of the Python implementation should be advised that the YAML portion
of a < 1.6.0 ASDF file containing null values may be modified in unexpected
ways when read or written.
