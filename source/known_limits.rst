.. _known-limits:

Known limits
============

The following is a catalogue of known limits in ASDF |version|.

Tree
----

While there is no hard limit on the size of the Tree, in most
practical implementations it will need to be read entirely into main
memory in order to interpret it, particularly to support forward
references.  This imposes a practical limit on its size relative to
the system memory on the machine.  It is not recommended to store
large data sets in the tree directly, instead it should reference
blocks.

Literal integer values in the Tree
----------------------------------

Different programming languages deal with numbers differently.  For
example, Python has arbitrary-length integers, while Javascript stores
all numbers as 64-bit double-precision floats.  It may be possible to
write long integers from Python into the Tree, and upon reading in
Javascript have undefined loss of information when reading those
values back in.

Therefore, for practical reasons, integer literals in the Tree must
be at most 52-bits.

As of version **1.3.0** of the standard, arbitrary precision integers are
supported using :ref:`integer <core/integer-1.0.0>`.  Like all tags, use of
this type requires library support.

Blocks
------

The maximum size of a block header is 65536 bytes.

Since the size of the block is stored in a 64-bit unsigned integer,
the largest possible block size is around 18 exabytes.  It is likely
that other limitations on file size, such as an operating system's
filesystem limitations, will be met long before that.
