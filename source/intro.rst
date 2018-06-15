Introduction
============

The Flexible Image Transport System (FITS) has been the de facto
standard for storing and exchanging astronomical data for decades, but
it is beginning to show its age.  Developed in the late 1970s, the
FITS authors made a number of implementation choices that, while
common at the time, are now seen to limit its utility for the needs of
modern science.  As astronomy moves into a more varied set of data
product types (data models) with richer and more complex metadata,
FITS is being pushed to its breaking point.  The issues with FITS are
outlined in great detail in [Thomas2015]_.

Newer formats, such as `VOTable
<http://www.ivoa.net/documents/VOTable/>`__ have partially addressed
the problem of richer, more structured metadata, by using tree
structures rather than flat key/value pairs.  However, those
text-based formats are unsuitable for storing large amounts of binary
data.  On the other end of the spectrum, formats such as `HDF5
<http://www.hdfgroup.org/HDF5/>`__ and `BLZ
<http://blaze.pydata.org/>`__ address problems
with large data sets and distributed computing, but don't really
address the metadata needs of an interchange format.  ASDF aims to
exist in the same middle ground that made FITS so successful, by being
a hybrid text and binary format: containing human editable metadata
for interchange, and raw binary data that is fast to load and use.
Unlike FITS, the metadata is highly structured and is designed
up-front for extensibility.

ASDF has the following explicit goals:

- It has a hierarchical metadata structure, made up of basic dynamic
  data types such as strings, numbers, lists and mappings.

- It has human-readable metadata that can be edited directly in place
  in the file.

- The structure of the data can be automatically validated using
  schema.

- It's designed for extensibility: new conventions may be used without
  breaking backward compatibility with tools that do not understand
  those conventions.  Versioning systems are used to prevent
  conflicting with alternative conventions.

- The binary array data (when compression is not used) is a raw memory
  dump, and techniques such as memory mapping can be used to
  efficiently access it.

- It is possible to read and write the file in as a stream, without
  requiring random access.

- It's built on top of industry standards, such as `YAML
  <http://www.yaml.org>`__ and `JSON Schema
  <http://www.json-schema.org>`__ to take advantage of a larger
  community working on the core problems of data representation.  This
  also makes it easier to support ASDF in new programming languages
  and environments by building on top of existing libraries.

- Since every ASDF file has the version of the specification to which
  it is written, it will be possible, through careful planning, to
  evolve the ASDF format over time, allowing for files that use new
  features while retaining backward compatibility with older tools.

ASDF is primarily intended as an interchange format for delivering
products from instruments to scientists or between scientists.  While
it is reasonably efficient to work with and transfer, it may not be
optimal for direct use on large data sets in distributed and high
performance computing environments.  That is explicitly not a goal of
the ASDF standard, as those requirements can sometimes be at odds with
the needs of an interchange format.  ASDF still has a place in those
environments as a delivery mechanism, even if it ultimately is not the
actual format on which the computing is performed.

Implementations
---------------

The ASDF standard is being developed concurrently with a `reference
implementation written in Python
<http://github.com/spacetelescope/asdf>`__.

There is also a work-in-progress `implementation for Go
<http://github.com/astrogo/asdf>`__ by Sebastian Binet.

Incorporated standards
----------------------

The ASDF format is built on top of a number of existing standards:

- `YAML 1.1 <http://yaml.org/spec/1.1/>`__

- JSON Schema Draft 4:

  - `Core <http://tools.ietf.org/html/draft-zyp-json-schema-04>`__

  - `Validation
    <http://tools.ietf.org/html/draft-fge-json-schema-validation-00>`__

  - `Hyper-Schema
    <http://tools.ietf.org/html/draft-luff-json-hyper-schema-00>`__

- `JSON Pointer <http://tools.ietf.org/html/rfc6901>`__

- `Semantic Versioning 2.0.0 <http://semver.org/spec/v2.0.0.html>`__

- `VOUnits (Units in the VO)
  <http://www.ivoa.net/documents/VOUnits/index.html>`__

- `Zlib Deflate compression <http://www.zlib.net/feldspar.html>`__

.. [Thomas2015] Thomas, B., Jenness. T. et al. (2015).
   Learning from FITS: Limitations in use in modern astronomical research.
   *Astronomy and Computing*, 12: 133-145.
   `doi:10.1016/j.ascom.2015.01.009 <https://doi.org/10.1016/j.ascom.2015.01.009>`__
