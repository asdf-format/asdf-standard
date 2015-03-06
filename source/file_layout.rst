Low-level file layout
=====================

The overall structure of a file is as follows (in order):

- :ref:`header`

- :ref:`tree`, optional

- Zero or more :ref:`block`

ASDF is a hybrid text and binary format.  The header and tree are
text, (specifically, in UTF-8), while the blocks are raw binary.

The low-level file layout is designed in such a way that the tree
section can be edited by hand, possibly changing its size, without
requiring changes in other parts of the file.  The same is not true
for resizing a block, which has an explicit size stored in the file
(except for, optionally, the last block).

Note also that, by design, an ASDF file containing no binary blocks is
also a completely standard and valid YAML file.

.. _header:

Header
------

All ASDF files must start with a short one-line header.  For example::

  #ASDF 0.1.0

It is made up of the following parts (described in EBNF form)::

  asdf_token = "#ASDF"
  major      = integer
  minor      = integer
  micro      = integer
  header     = asdf_token " " major "." minor "." micro ["\r"] "\n"

- ``asdf_token``: The constant string ``#ASDF``.  This can be used
  to quickly identify the file as an ASDF file by reading the first 5
  bytes.  It begins with a ``#`` so it will be treated as a YAML
  comment such that the :ref:`header` and the :ref:`tree` together
  form a valid YAML file.

- ``major``: The major version.

- ``minor``: The minor version.

- ``micro``: The bugfix release version.

.. _tree:

Tree
----

The tree stores structured information using `YAML Ain’t Markup
Language (YAML™) 1.1 <http://yaml.org/spec/1.1/>`__ syntax.  While it
is the main part of most ASDF files, it is entirely optional, and a
ASDF file may skip it completely.  This is useful for creating files
in :ref:`exploded`.  Interpreting the contents of this section is
described in greater detail in :ref:`tree-in-depth`.  This section
only deals with the serialized representation of the tree, not its
logical contents.

The tree is always encoded in UTF-8, without an explicit byteorder
marker (BOM). Newlines in the tree may be either DOS (``"\r\n"``) or
UNIX (``"\n"``) format.

In ASDF |version|, the tree must be encoded in `YAML version 1.1
<http://yaml.org/spec/1.1/>`__.  At the time of this writing, the
latest version of the YAML specification is 1.2, however most YAML
parsers only support YAML 1.1, and the benefits of YAML 1.2 are minor.
Therefore, for maximum portability, ASDF requires that the YAML is
encoded in YAML 1.1.  To declare that YAML 1.1 is being used, the tree
must begin with the following line::

    %YAML 1.1

The tree must contain exactly one YAML document, starting with ``---``
(YAML document start marker) and ending with ``...`` (YAML document
end marker), each on their own line.  Between these two markers is the
YAML content.  For example::

      %YAML 1.1
      %TAG ! tag:stsci.edu:asdf/0.1.0/
      --- !core/asdf
      data: !core/ndarray
        source: 0
        datatype: float64
        shape: [1024, 1024]
      ...

The size of the tree is not explicitly specified in the file, so that
it can easily be edited by hand.  Therefore, ASDF parsers must search
for the end of the tree by looking for the end-of-document marker
(``...``) on its own line.  For example, the following regular
expression may be used to find the end of the tree::

   \r?\n...\r?\n

Though not required, the tree should be followed by some unused space
to allow for the tree to be updated and increased in size without
performing an insertion operation in the file.  It also may be
desirable to align the start of the first block to a filesystem block
boundary.  This empty space may be filled with any content (as long as
it doesn't contain the ``block_magic_token`` described in
:ref:`block`).  It is recommended that the content is made up of space
characters (``0x20``) so it appears as empty space when viewing the
file.

.. _block:

Blocks
------

Following the tree and some empty space, or immediately following the
header, there are zero or more binary blocks.

Blocks represent a contiguous chunk of binary data and nothing more.
Information about how to interpret the block, such as the data type or
array shape, is stored entirely in ``ndarray`` structures in the tree,
as described in :ref:`ndarray
<http://stsci.edu/schemas/asdf/0.1.0/core/ndarray>`.  This allows
for a very flexible type system on top of a very simple approach to
memory management within the file.  It also allows for new extensions
to ASDF that might interpret the raw binary data in ways that are yet
to be defined.

There may be an arbitrary amount of unused space between the end of
the tree and the first block.  To find the beginning of the first
block, ASDF parsers should search from the end of the tree for the
first occurrence of the ``block_magic_token``.  If the file contains
no tree, the first block must begin immediately after the header with
no padding.

.. _block-header:

Block header
^^^^^^^^^^^^

Each block begins with the following header:

- ``block_magic_token`` (4 bytes): Indicates the start of the block.
  This allows the file to contain some unused space in which to grow
  the tree, and to perform consistency checks when jumping from one
  block to the next.  It is made up of the following 4 8-bit characters:

  - in hexadecimal: d3, 42, 4c, 4b
  - in ascii: ``"\323BLK"``

- ``header_size`` (16-bit unsigned integer, big endian): Indicates the
  size of the remainder of the header (not including the length of the
  ``header_size`` entry itself or the ``block_magic_token``), in bytes.
  It is stored explicitly in the header itself so that the header may be
  enlarged in a future version of the ASDF standard while retaining
  backward compatibility.  Importantly, ASDF parsers should not assume
  a fixed size of the header, but should obey the ``header_size``
  defined in the file.  In ASDF version 0.1, this should be at least
  36, but may be larger, for example to align the beginning of the
  block content with a file system block boundary.

- ``flags`` (32-bit unsigned integer, big-endian): A bit field
  containing flags (described below).

- ``allocated_size`` (64-bit unsigned integer, big-endian): The amount
  of space allocated for the block (not including the header), in
  bytes.

- ``used_size`` (64-bit unsigned integer, big-endian): The amount of
  used space for the block on disk (not including the header), in
  bytes.

- ``memory_size`` (64-bit unsigned integer, big-endian): The size of
  the block when decoded, in bytes.  If ``encoding`` is all zeros
  (indicating no encoding), it **must** be equal to ``used_size``.  If
  there is an encoding, this is the size of the decoded block data,
  which **may** be different from the size of the encoded block in the
  ASDF file.

- ``checksum`` (64-bit unsigned integer, big-endian): An optional MD5
  checksum of the used data in the block.  The special value of 0
  indicates that no checksum verification should be performed.  *TBD*.

Flags
^^^^^

The following bit flags are understood in the ``flags`` field:

- ``STREAMED`` (0x1): When set, the block is in streaming mode, and it
  extends to the end of the file.  When set, the ``allocated_size``,
  ``used_size`` and ``memory_size`` fields are ignored.  By necessity,
  any block with the ``STREAMED`` bit set must be the last block in
  the file.

- ``ENCODED`` (0x2): When set, the block has an explicit encoding (or
  compression) applied.  In this case, ``used_size`` indicates the
  number of bytes in the block on disk, and ``mem_size`` indicates the
  number of bytes in the block in memory.  See :ref:`block-encoding`
  for more information.

The ``STREAMED`` and ``ENCODED`` flags are mutually exclusive and may
not both be set.

Block content
^^^^^^^^^^^^^

Immediately following the block header, there are exactly
``used_space`` bytes of meaningful data, followed by
``allocated_space - used_space`` bytes of unused data.  The exact
content of the unused data is not enforced.  The ability to have gaps
of unused space allows an ASDF writer to reduce the number of disk
operations when updating the file.

.. _block-encoding:

Block encoding
--------------

By default, blocks are stored on disk as contiguous arrays, so they
can be easily memory-mapped.  However, ASDF also supports "encoded"
blocks in order to support compression or other transformations from
on-disk to in-memory representations.

When the ``ENCODED`` flag is ``True``, the block data begins with a
chunk of YAML describing the encoding chain.  This YAML may have any
length, and ends with the standard YAML end marker::

  \r?\n...\r?\n

Following this YAML chunk is the arbitrary encoded binary data.  In
this case, the ``used_size`` value of the block header includes the
size of this YAML encoding chain specifier and the following binary
blob.

.. note::

    YAML is used here so that encoding specifiers can be as flexible
    as possible.  However, unlike the YAML tree at the beginning of
    the file, this YAML chunk is not designed to be "user editable".

This YAML chunk represents an encoding chain, which is a list of
encodings, applied in the given order to encode and the reverse order
to decode.  Each entry is a single string ``name`` or a pair of the
form ``(name, args)``, where ``name`` is a the name of the encoding
and ``args`` is an optional dictionary of arguments for the encoding.

For example, the following means that ``zlib`` compression is be
applied to the block::

    [zlib]

The following example reorders the given array into tiles of size (32
x 32) before applying ``zlib`` compression, which may give better
compression for typical astronomy images::

    [[tile, {shape: [32, 32]}], zlib]

The following example is very similar to the compression scheme in
CFITSIO, where the image is tiled, and then each tile is lossily
quantized before being run through a standard lossless compression
scheme::

    [[tile, {shape: [32, 32]}], [quantize, {quality: 4}], zlib]

At each step of an encoding chain, the data can either be represented
as an array, meaning it still includes basic metadata such as the the
shape and datatype, or as binary, which is just a stream of bytes.
With this in mind, ASDF encodings fall into three categories:

  - array-to-array encodings transform an array into another array
  - array-to-binary encodings transform an array into a binary
    representation.
  - binary-to-binary encodings transform a stream of binary input into
    binary output.

Encoding chains must be ordered such that the output of one encoding
matches the input of the next.  If the chain consists only of
"binary-to-binary" encodings, an implicit "null" array-to-binary
encoding is inserted at the front that is simply the in-memory
representation of the array.

The ASDF standard defines a number of built-in encodings below.  Other
encodings may be used for application-specific purposes, and ASDF
parsers must handle such unknown encodings gracefully.  If an ASDF
parser encounters an unknown encoding name, it should report back that
it can not decode the block.  It should not, however, consider the
YAML tree and other blocks in the file to be invalid or inaccessible.

Built-in array-to-array encodings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``tile``: This rearranges the ordering of the elements in an
  *n*-dimensional array into *n*-dimensional tiles of the given shape.
  It has the following required arguments:

  - ``shape``: The shape of each tile.  It is a list of integers of
    length *N*, where *N* is the number of dimensions in the input
    array.

  - ``original_shape``: The original shape of the input array, so it
    can be correctly reconstituted upon decoding.

  - ``item_size``: The size of each item of the array, in bytes.

  If any of the dimensions ``original_shape`` are not an exact
  multiple of the corresponding dimension in ``shape``, the tiles in
  the non-zero edge of each dimension are padded so each tile is
  exactly of size ``shape``.  These extra values are discarded upon
  decoding.

Built-in array-to-binary encodings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``quantize``: A lossy compression algorithm that converts floating
  point values to integers with a global scale and offset.  The ASDF
  standard does not define the algorithm used to perform the
  quantization and dithering of the data, only the
  on-disk-representation and the decoding.

  The following arguments are required in the YAML encoding descriptor:

  - ``dtype``: Must be 32 or 64, representing the bits in the original
    floating-point values.

  - ``original_shape``: A list of integers representing the shape of
    the original array.

  A quantized data stream consists of *N* chunks, each with the
  following binary header:

  - ``encoded_bits`` (unsigned 8-bit integer): The number of bits for
    each encoded value.
  - ``offset`` (64-bit double-precision float, big-endian): The offset
    value of each item.
  - ``scale`` (64-bit double-precision float, big-endian): The scale
    value of each item.
  - ``nvalues`` (64-bit unsigned integer, big-endian): The number of
    values in the chunk.

  The header is then followed by ``encoded_bits * nvalues`` bits of
  data, zero-padded to the nearest byte.  Each value is a
  twos-complement signed integer, ``encoded_bits`` long and
  big-endian.  The bits are packed closely together, i.e. if
  ``encoded_bits`` is not a multiple of 8, the values do not begin on
  byte boundaries.  Each value is decoded using the following
  calculation::

    ``decoded = (encoded * scale) + offset``

  Immediately following each chunk may either be another chunk or the
  end of the binary data.

Built-in binary-to-binary encodings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``zlib``: A lossless compression algorithm.  It is widely used,
  patent-unencumbered, and has an implementation released under a
  permissive license in `zlib <http://www.zlib.net/>`__.  This
  encoding takes no arguments.

.. _exploded:

Exploded form
-------------

Exploded form expands a self-contained ASDF file into multiple files:

- An ASDF file containing only the header and tree, which by design is
  also a valid YAML file.

- *n* ASDF files, each containing a single block.

Exploded form is useful in the following scenarios:

- Not all text editors may handle the hybrid text and binary nature of
  the ASDF file, and therefore either can't open an ASDF file or would
  break an ASDF file upon saving.  In this scenario, a user may explode
  the ASDF file, edit the YAML portion as a pure YAML file, and
  implode the parts back together.

- Over a network protocol, such as HTTP, a client may only need to
  access some of the blocks.  While reading a subset of the file can
  be done using HTTP ``Range`` headers, it still requires one (small)
  request per block to "jump" through the file to determine the start
  location of each block.  This can become time-consuming over a
  high-latency network if there are many blocks.  Exploded form allows
  each block to be requested directly by a specific URI.

- An ASDF writer may stream a table to disk, when the size of the table
  is not known at the outset.  Using exploded form simplifies this,
  since a standalone file containing a single table can be iteratively
  appended to without worrying about any blocks that may follow it.

Exploded form describes a convention for storing ASDF file content in
multiple files, but it does not require any additions to the file
format itself.  There is nothing indicating that an ASDF file is in
exploded form, other than the fact that some or all of its blocks come
from external files.  The exact way in which a file is exploded is up
to the library and tools implementing the standard.  In the simplest
scenario, to explode a file, each :ref:`ndarray source property
<http://stsci.edu/schemas/asdf/0.1.0/core/ndarray/anyOf/1/properties/source>`
in the tree is converted from a local block reference into a relative
URI.
