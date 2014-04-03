.. _known-limits:

Known limits
============

The following is a catalogue of known limits in FINF |version|.

Tree
----

While there is no hard limit on the size of the tree, in most
practical implementations it will need to be read entirely into main
memory in order to interpret it, imposing a practical limit on its
size.  It is not recommended to store large data sets in the tree
directly, instead it should reference blocks.

Blocks
------

Since the size of the block is stored in a 64-bit unsigned integer,
the largest possible block size is 18,446,744,073,709,551,616 bytes,
or 18 exabytes.  It is likely that other limitations on file size,
such as an operating system's filesystem limitations, will be met long
before that.
