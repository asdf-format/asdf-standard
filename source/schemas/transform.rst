.. _transform-schema:

Transform
=========

The ``transform`` module contains schema used to describe transformations.

:category:`Requires:`

:doc:`core`

Basics
------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/transform-1.1.0
   stsci.edu/asdf/transform/generic-1.1.0
   stsci.edu/asdf/transform/identity-1.1.0
   stsci.edu/asdf/transform/constant-1.2.0
   stsci.edu/asdf/transform/domain-1.0.0

Compound transformations
------------------------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/compose-1.1.0
   stsci.edu/asdf/transform/concatenate-1.1.0
   stsci.edu/asdf/transform/remap_axes-1.1.0

Arithmetic operations
---------------------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/add-1.1.0
   stsci.edu/asdf/transform/subtract-1.1.0
   stsci.edu/asdf/transform/multiply-1.1.0
   stsci.edu/asdf/transform/divide-1.1.0
   stsci.edu/asdf/transform/power-1.1.0

Simple Transforms
-----------------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/shift-1.2.0
   stsci.edu/asdf/transform/scale-1.2.0

Projections
-----------

Affine
^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/affine-1.2.0
   stsci.edu/asdf/transform/rotate2d-1.2.0
   stsci.edu/asdf/transform/rotate3d-1.2.0

Zenithal (azimuthal)
^^^^^^^^^^^^^^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/zenithal-1.1.0
   stsci.edu/asdf/transform/gnomonic-1.1.0
   stsci.edu/asdf/transform/zenithal_perspective-1.2.0
   stsci.edu/asdf/transform/slant_zenithal_perspective-1.2.0
   stsci.edu/asdf/transform/stereographic-1.1.0
   stsci.edu/asdf/transform/slant_orthographic-1.1.0
   stsci.edu/asdf/transform/zenithal_equidistant-1.1.0
   stsci.edu/asdf/transform/zenithal_equal_area-1.1.0
   stsci.edu/asdf/transform/airy-1.1.0

Cylindrical
^^^^^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/cylindrical-1.1.0
   stsci.edu/asdf/transform/cylindrical_perspective-1.2.0
   stsci.edu/asdf/transform/cylindrical_equal_area-1.2.0
   stsci.edu/asdf/transform/plate_carree-1.1.0
   stsci.edu/asdf/transform/mercator-1.1.0

Pseudocylindrical
^^^^^^^^^^^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/pseudocylindrical-1.1.0
   stsci.edu/asdf/transform/sanson_flamsteed-1.1.0
   stsci.edu/asdf/transform/parabolic-1.1.0
   stsci.edu/asdf/transform/molleweide-1.1.0
   stsci.edu/asdf/transform/hammer_aitoff-1.1.0

Conic
^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/conic-1.2.0
   stsci.edu/asdf/transform/conic_perspective-1.2.0
   stsci.edu/asdf/transform/conic_equidistant-1.2.0
   stsci.edu/asdf/transform/conic_equal_area-1.2.0
   stsci.edu/asdf/transform/conic_orthomorphic-1.2.0

Pseudoconic
^^^^^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/pseudoconic-1.1.0
   stsci.edu/asdf/transform/bonne_equal_area-1.2.0
   stsci.edu/asdf/transform/polyconic-1.1.0

Quadcube
^^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/quadcube-1.1.0
   stsci.edu/asdf/transform/tangential_spherical_cube-1.1.0
   stsci.edu/asdf/transform/cobe_quad_spherical_cube-1.1.0
   stsci.edu/asdf/transform/quad_spherical_cube-1.1.0

HEALPix
^^^^^^^

.. asdf-autoschemas::

   stsci.edu/asdf/transform/healpix-1.1.0
   stsci.edu/asdf/transform/healpix_polar-1.1.0

Polynomials
-----------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/polynomial-1.2.0

Regions and labels
------------------

.. asdf-autoschemas::

   stsci.edu/asdf/transform/regions_selector-1.1.0
   stsci.edu/asdf/transform/label_mapper-1.1.0
