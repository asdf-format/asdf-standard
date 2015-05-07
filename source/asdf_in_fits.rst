Appendix A: Embedding ASDF in FITS
==================================

While ASDF is designed to replace all of the existing use cases of
FITS, there will still be cases where files need to be produced in
FITS.  Even then, it would be nice to take advantage of the
highly-structured nature of ASDF to store content that can not easily
be represented in FITS in a FITS file.  This appendix describes a
convention for embedding ASDF content in a FITS file.

The content of the ASDF file is placed in the data portion of an extra
image extension named ``ASDF`` (``EXTNAME = 'ASDF'``).  (By
convention, the datatype is unsigned 8-bit integers (``BITPIX = 8``)
and is one-dimensional (``NAXIS = 1``), but this is not strictly
necessary.)

Rather than including a copy of the large data arrays in the ASDF
extension, the ASDF content may refer to binary data stored in regular
FITS extensions elsewhere in the same file.  The convention for doing
this is to set the ``source`` property of a :ref:`ndarray
<http://stsci.edu/schemas/asdf/0.1.0/core/ndarray>` object to a
special string identifier for a FITS reference.  These values come in
two forms:

- ``fits:EXTNAME,EXTVER``: Where ``EXTNAME`` and ``EXTVER`` uniquely
  identify a FITS extension.

- ``fits:INDEX``: Where ``INDEX`` is the zero-based index of a FITS
  extension.

The ``fits:EXTNAME,EXTVER`` form is preferred, since it allows for
rearranging the FITS extensions in the file without the need to update
the content of the ``ASDF`` extension, and thus such rearrangements
could be performed by a non-ASDF-aware FITS library.

Such "FITS references" simply point to the binary content of the data
portion of a FITS header/data unit.  There is no enforcement that the
``datatype`` of the ASDF :ref:`ndarray
<http://stsci.edu/schemas/asdf/0.1.0/core/ndarray>` matches the
``BITPIX`` of the FITS extension, or expectation that an explicit
conversion would be performed if they don't match.  It is up to the
writer of the file to keep the ASDF and FITS datatype descriptions in
sync.

The following is a schematic of an example FITS file with an ASDF
extension.  The ASDF content references the binary data in two FITS
extensions elsewhere in the file.

.. code::

  HDU 0:
  ┌─────────────────────────────────────┐
  │SIMPLE  = T                          │
  │BITPIX  = -64                        │
  │NAXIS   = 2                          │
  │NAXIS1  = 512                        │
  │NAXIS2  = 512                        │
  │EXTEND  = T                          │
  │EXTNAME = 'SCI     '                 │
  │END                                  │
  ├─────────────────────────────────────┤
  │...data...                           │<──┐
  └─────────────────────────────────────┘   │
  HDU 1:                                    │
  ┌─────────────────────────────────────┐   │
  │XTENSION= 'IMAGE   '                 │   │
  │BITPIX  = -64                        │   │
  │NAXIS   = 2                          │   │
  │NAXIS1  = 512                        │   │
  │NAXIS2  = 512                        │   │
  │EXTNAME = 'DQ      '                 │   │
  │END                                  │   │
  ├─────────────────────────────────────┤   │
  │...data...                           │<──┼───┐
  └─────────────────────────────────────┘   │   │
  HDU 2:                                    │   │
  ┌─────────────────────────────────────┐   │   │
  │XTENSION= 'IMAGE   '                 │   │   │
  │BITPIX  = 8                          │   │   │
  │NAXIS   = 1                          │   │   │
  │NAXIS1  = 361                        │   │   │
  │EXTNAME = 'ASDF    '                 │   │   │
  │END                                  │   │   │
  ├─────────────────────────────────────┤   │   │
  │#ASDF 0.1.0                          │   │   │
  │%YAML 1.1                            │   │   │
  │%TAG ! tag:stsci.edu:asdf/0.1.0/     │   │   │
  │--- !core/asdf                       │   │   │
  │model:                               │   │   │
  │  sci:                               │   │   │
  │    data: !core/ndarray              │   │   │
  │      source: fits:SCI,1   ──────────┼───┘   │
  │      datatype: float64              │       │
  │      byteorder: little              │       │
  │      shape: [512]                   │       │
  │    wcs: ...WCS info...              │       │
  │  dq:                                │       │
  │    data: !core/ndarray              │       │
  │      source: fits:DQ,1    ──────────┼───────┘
  │      datatype: float64              │
  │      byteorder: little              │
  │      shape: [512]                   │
  │    wcs: ...WCS info...              │
  │...                                  │
  └─────────────────────────────────────┘
