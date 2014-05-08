Low-level file layout
=====================

The overall structure of a file is as follows (in order):

- :ref:`header`

- :ref:`tree`, optional

- Zero or more :ref:`block`

FINF is a hybrid text and binary format.  The header and tree are
text, (specifically, in UTF-8), while the blocks are raw binary.

The low-level file layout is designed in such a way that the tree
section can be edited by hand, possibly changing its size, without
requiring changes in other parts of the file.  The same is not true
for resizing a block, which has an explicit size stored in the file.

Note also that, by design, a FINF file containing no binary blocks is
also a completely valid YAML file.

.. _header:

Header
------

All FINF files must start with a short one-line header.  For example::

  %FINF 0.1.0

It is made up of the following parts::

  <FINF_TOKEN> <SPACE> major <DOT> minor <DOT> micro <NEWLINE>

- ``<FINF_TOKEN>``: The constant string ``%FINF``.  This can be used
  to quickly identify the file as a FINF file by reading the first 5
  bytes.  It begins with a ``%`` so it will be treated as a YAML
  comment such that the :ref:`header` and the :ref:`tree` together
  form a valid YAML file.

- ``<SPACE>``: The constant string ``␣`` (ASCII 0x20).

- ``<DOT>``: The constant string ``.`` (ASCII 0x2e).

- ``major``: The major version.  Must be a non-negative integer
  matching the regular expression :regexp:`[0-9]+`.

- ``minor``: The minor version.  Must be a non-negative integer
  matching the regular expression :regexp:`[0-9]+`.

- ``micro``: The bugfix release version.  Must be a non-negative
  integer matching the regular expression :regexp:`[0-9]+`.

- ``<NEWLINE>``: A UNIX (``\n``) or DOS (``\r\n``) line ending.

.. _tree:

Tree
----

The tree stores structured information using YAML Ain’t Markup
Language (YAML™) syntax.  While it is the main part of most FINF
files, it is entirely optional, and a FINF file may skip it
completely.  This is useful for sharing files in :ref:`exploded`.
Interpreting the contents of this section is described in greater
detail in :ref:`tree-in-depth`.  This section below only deals with
the serialized representation of the tree, not its logical contents.

The tree is always encoded in UTF-8, without an explicit byteorder
marker (BOM).

Newlines in the tree may be either DOS (``\r\n``) or UNIX (``\n``)
format.

In FINF |version|, the tree must be encoded in `YAML version 1.1
<http://yaml.org/spec/1.1/>`__.  At the time of this writing, the
latest version of the YAML specification is 1.2, however most YAML
parsers only support YAML 1.1, and the benefits of YAML 1.2 are minor.
Therefore, for maximum portability, FINF requires that the YAML is
encoded in YAML 1.1.  To declare that YAML 1.1 is being used, the tree
must begin with the following line::

    %YAML 1.1

The tree must contain exactly one YAML document, starting with ``---``
(YAML document start marker) and ending with ``...`` (YAML document
end marker), each on their own line.  Between these two markers is the
YAML content.  For example::

      %YAML 1.1
      %TAG ! tag:stsci.edu:finf/0.1.0/
      --- !core/finf
      data: !core/ndarray
        source: 0
        dtype: float64
        shape: [1024, 1024]
      ...

The size of the tree is not explicitly specified in the file, so that
it can easily be edited by hand.  Therefore, FINF parsers must search
for the end of the tree by looking for the end-of-document marker
(``...``) on its own line.  The following regular expression may be
used to find the end of the tree::

   \r?\n...\r?\n

Though not required, the tree should be followed by some unused space
to allow for the tree to be updated and increased in size without
performing an insertion operation in the file.  It also may be
desirable to align the start of the first block to a filesystem block
boundary.  This empty space may be filled with any content (as long as
it doesn't contain the block magic token described below), but it is
recommended to be space characters (``0x20``) so it appears as empty
space when viewing the file.

.. _block:

Blocks
------

Following the tree and some empty space, or immediately following the
header, there are zero or more binary blocks.

Blocks represent a contiguous chunk of binary data and nothing more.
Information about how to interpret the block, such as the data type or
array shape, is stored entirely in ``ndarray`` structures in the tree,
as described in :ref:`ndarray
<http://www.stsci.edu/schemas/finf/0.1.0/core/ndarray>`.  This allows for a
very flexible type system on top of a very simple approach to memory
management within the file.  It also allows for new extensions to FINF
that might interpret the raw binary data in ways that have not yet
been devised.

There may be an arbitrary amount of unused space between the end of
the tree and the first block.  To find the beginning of the first
block, FINF parsers should search from the end of the tree for the
first occurrence of the ``block_magic_token``.  If the file contains
no tree, the first block must begin immediately after the header with
no padding.

.. _block-header:

Block header
^^^^^^^^^^^^

Each block begins with the following header:

- ``block_magic_token`` (4 bytes): Indicates the start of the block.
  This allows the file to contain some unused space in which to grow
  the tree, and to perform sanity checks when jumping from one block
  to the next.

  +---------+--------+------+------+------+
  |**Hex**  |``89``  |``42``|``4c``|``4b``|
  +---------+--------+------+------+------+
  |**ASCII**|``\211``|``B`` |``L`` |``K`` |
  +---------+--------+------+------+------+

- ``header_size`` (16-bit unsigned integer, big endian): Indicates the
  size of the remainder of the header (not including the length of the
  ``header_size`` entry itself or the ``block_magic_token``).  It is
  stored explicitly in the header itself so that the header may be
  enlarged in a future version of the FINF standard while retaining
  backward compatibility.  Parsers should not assume a fixed size of
  the header.  In FINF version 0.1, this should be at least 29, but
  may be larger, for example to align the beginning of the block
  content with a file system block boundary.

- ``allocated_size`` (64-bit unsigned integer, big-endian): The amount
  of space allocated for the block (not including the header), in
  bytes.

- ``used_size`` (64-bit unsigned integer, big-endian): The amount of
  used space for the block (not including the header), in bytes.

- ``checksum`` (64-bit unsigned integer, big-endian): An optional MD5
  checksum of the used data in the block.  The special value of 0
  indicates that no checksum verification should be performed.  *TBD*.

- ``encoding`` (16-byte character string): A way to indicate how the
  buffer is compressed or encoded.  *TBD*.

Block content
^^^^^^^^^^^^^

Immediately following the block header, there are exactly
``used_space`` bytes of meaningful data, followed by
``allocated_space - used_space`` bytes of unused data.  The exact
content of the unused data is not enforced.  The ability to have gaps
of unused space allows a FINF writer to reduce the number of disk
operations necessary to update the file.

.. _exploded:

Exploded form
-------------

Exploded form expands a self-contained FINF file into multiple files:

- A FINF file containing only the header and tree, which by design is
  also a valid YAML file.

- *n* FINF files, each containing a single block.

Exploded form is useful in the following scenarios:

- A given text editor does not handle the "hybrid" nature of the FINF
  file, and therefore either can't open a FINF file or breaks FINF
  files upon saving.  In this scenario, a user may explode the FINF
  file, edit the YAML portion as a pure YAML file, and implode the
  parts back together.

- Over a network protocol, such as HTTP, a client may only need to
  access some of the blocks.  While reading a subset of the file can
  be done using HTTP ``Range`` headers, it still requires one (small)
  request per block to "jump" through the file to determine the start
  location of each block.  This can become time-consuming over a
  high-latency network if there are many blocks.  Exploded form allows
  each block to be requested directly by a specific URI.

- A FINF writer may stream a table to disk, when the size of the table
  is not known at the outset.  Using exploded form simplifies this,
  since a standalone file containing a single table can be iteratively
  appended to without worrying about any blocks that may follow it.

Exploded form describes a convention for storing FINF file content in
multiple files, but it does not define any changes to the file format
itself.  There is nothing indicating that a FINF file is in exploded
form, other than the fact that some or all of its block references
refer to external files.  The exact way in which a file is exploded is
up to the library and tools implementing the standard.  In the most
common scenario, to explode a file, each :ref:`ndarray source property
<http://www.stsci.edu/schemas/finf/0.1.0/core/ndarray/source>` in the tree
is converted from a local block reference into a relative URI.  Each
FINF file has exactly the same content as the :ref:`block` in the
original file (including the block header), but without the
unallocated space.
