Introduction
============

Flexible Image Transport System (FITS) has been the de facto standard
for storing and exchanging astronomical data for decades, but it is
beginning to show its age.

.. note::

   TODO: Eventually, this will become a complete laundry list of FITS
   shortcomings, based on "The Future of Astronomical Data
   Formats I. Learning from FITS" and hopefully how FINF will address
   them.

Newer formats, such as VOTable (ref) and FITSML (ref), have at least
partially addressed the problem of richer, more structured metadata,
by using XML tree structures.  However, those formats are unsuitable
for storing large amounts of binary data.  On the other end of the
spectrum, formats such as HDF5 (ref) and Blaze (ref) address problems
with large data sets and distributed computing, but don't really
address the metadata needs of an interchange format.  FINF aims to
succeed on both fronts: one that stores rich structured metadata for
interchange, and contains raw binary data that is fast to load and
use.

FINF has the following explicit goals:

    - It has a hierarchical metadata structure, made up of basic
      dynamic data types such as lists and mappings.

    - It has human-readable metadata that can be edited directly in
      place in the file.

    - The structure of the data can be easily validated using schema.

    - It's easily extensible with new conventions without breaking
      backward compatibility with tools that do not understand those
      conventions or conflicting with other ad hoc conventions.

    - The binary array data (when compression is not used) is "raw",
      and techniques such as memory mapping can be used to efficiently
      access it.

    - It is possible to "stream" to disk or over a network without
      seeking.

    - It's built on top of industry standards, such as YAML and JSON
      Schema, to take advantage of a larger community working on the
      core problems, and to make it easier to support in new
      programming languages and environments.

Implementations
---------------

FINF currently has a `reference implementation written in Python
<http://github.com/spacetelescope/pyfinf>`__, and a C implementation
is planned.
