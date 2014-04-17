.. _extending-finf:

Extending FINF
==============

FINF is designed to be extensible so outside teams can add their own
types and structures while retaining compatibility with tools that
don't understand those conventions.

.. note::

    **Point for discussion**: Where should we recommend "outside
    groups" put domain-specific structures?  One of the shortcomings
    of FITS is that the namespace gets polluted with competing
    external conventions, and some of those conventions ultimately
    name clash.  Should we enforce that all extensions go under a
    special property at the top-level of the tree, for example, called
    "extensions"?  Or should we have a convention that every extension
    should first go under an organization name, such as "stsci.edu"?
    I think it's important to get this right early, so we don't end
    up having competing things under the same name.  At the same time,
    it needs to be a convention that is not too rigid.

TODO: This section will describe making a custom tag type for FINF.
