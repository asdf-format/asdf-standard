How does FINF address deficiencies of FITS
==========================================

This document is based on the paper, which at the time of this writing
is in a prerelease form:

   Thomas, B., Jenness, T., et al, 2014.  *The Future of Astronomical
   Data Formats I. Learning from FITS*.  Prepublished.
   `https://github.com/timj/aandc-fits/releases
   <https://github.com/timj/aandc-fits/releases>`__.

Below are a number of identified deficiencies of FITS for modern
astronomical data processing, along with an explanation of how FINF
addresses that issue.

No versioning
-------------

  There is no standard means which allows the FITS file to communicate
  the formatting version it conforms to.  The only keyword which implies
  any type of format is ``SIMPLE`` which is set to ``T``, or true. The
  comment indicates that the file conforms to "Standard FITS
  format", but what indeed is that "Standard"?  We cannot know if the
  implied standard is actually 3.0 or some earlier (or later!)
  version.

FINF is versioned at a number of different levels.  The low-level file
layout has a version.  All binary headers in the format have an
explicit size in the file itself, so it will be possible to enlarge
these headers in the future while still allowing older FINF readers to
support new versions of FINF, as long as support for new features is
not required.

Each typed (tagged) entry in the tree is associated with a version.
It is possible to mix tags from multiple versions within the same
file.  For example, a group may decide that the unit format as defined
in the FINF standard version X is insufficient for their needs.  They
may define a new tag for their extended unit format, while providing a
backward compatible version of the same unit in FINF standard form.

  As there is no versioning to effectively declare deprecated
  structures in the format finally "illegal", the upshot is a
  fragmenting the FITS format through inaction rather than deliberate
  design.

Since the FINF format has a version number, it will be possible to
deprecate features in future versions of the standard.  FINF writers
may choose to continue to write the deprecated content for backward
compatibility, but it will be possible to identify and warn about the
use of these deprecated features.
