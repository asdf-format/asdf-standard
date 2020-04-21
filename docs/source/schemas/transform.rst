.. _transform-schema:

Transform
=========

The ``transform`` module contains schema used to describe transformations.

Basics
------

.. asdf-autoschemas::

   transform/constant-1.3.0
   transform/generic-1.2.0
   transform/identity-1.2.0

Simple Transforms
-----------------

.. asdf-autoschemas::

   transform/multiply-1.2.0
   transform/rotate2d-1.3.0
   transform/scale-1.2.0
   transform/shift-1.2.0

Compound Transforms
-------------------

.. asdf-autoschemas::

   transform/add-1.2.0
   transform/compose-1.2.0
   transform/concatenate-1.2.0
   transform/divide-1.2.0
   transform/power-1.2.0
   transform/remap_axes-1.2.0
   transform/subtract-1.2.0

Analytical Models
-----------------

.. asdf-autoschemas::

   transform/fix_inputs-1.2.0
   transform/math_functions-1.0.0
   transform/multiplyscale-1.0.0
   transform/rotate_sequence_3d-1.0.0
   transform/tabular-1.2.0

Functional Models
-----------------

.. asdf-autoschemas::

   transform/airy_disk2d-1.0.0
   transform/box1d-1.0.0
   transform/box2d-1.0.0
   transform/disk2d-1.0.0
   transform/ellipse2d-1.0.0
   transform/exponential1d-1.0.0
   transform/gaussian1d-1.0.0
   transform/gaussian2d-1.0.0
   transform/logarithmic1d-1.0.0
   transform/lorentz1d-1.0.0
   transform/ricker_wavelet1d-1.0.0
   transform/ricker_wavelet2d-1.0.0
   transform/ring2d-1.0.0
   transform/sine1d-1.0.0
   transform/trapezoid1d-1.0.0
   transform/trapezoid_disk2d-1.0.0

Physical Models
---------------

.. asdf-autoschemas::

   transform/blackbody-1.0.0
   transform/drude1d-1.0.0
   transform/king_projected_analytic1d-1.0.0
   transform/moffat1d-1.0.0
   transform/moffat2d-1.0.0
   transform/plummer1d-1.0.0
   transform/red_shift_scale_factor-1.0.0
   transform/sersic1d-1.0.0
   transform/sersic2d-1.0.0
   transform/voigt1d-1.0.0

Polynomials
-----------

.. asdf-autoschemas::

   transform/linear1d-1.0.0
   transform/ortho_polynomial-1.0.0
   transform/planar2d-1.0.0
   transform/polynomial-1.2.0

Projections
-----------

Affine
^^^^^^

.. asdf-autoschemas::

   transform/affine-1.3.0
   transform/rotate3d-1.3.0

Conic
^^^^^

.. asdf-autoschemas::

   transform/conic_equal_area-1.3.0
   transform/conic_equidistant-1.3.0
   transform/conic_orthomorphic-1.3.0
   transform/conic_perspective-1.3.0

Cylindrical
^^^^^^^^^^^

.. asdf-autoschemas::

   transform/cylindrical_equal_area-1.3.0
   transform/cylindrical_perspective-1.3.0
   transform/mercator-1.2.0
   transform/plate_carree-1.2.0

HEALPix
^^^^^^^

.. asdf-autoschemas::

   transform/healpix-1.2.0
   transform/healpix_polar-1.2.0

Pseudoconic
^^^^^^^^^^^

.. asdf-autoschemas::

   transform/bonne_equal_area-1.3.0
   transform/polyconic-1.2.0

Pseudocylindrical
^^^^^^^^^^^^^^^^^

.. asdf-autoschemas::

   transform/hammer_aitoff-1.2.0
   transform/molleweide-1.2.0
   transform/parabolic-1.2.0
   transform/sanson_flamsteed-1.2.0

Quadcube
^^^^^^^^

.. asdf-autoschemas::

   transform/cobe_quad_spherical_cube-1.2.0
   transform/quad_spherical_cube-1.2.0
   transform/tangential_spherical_cube-1.2.0

Zenithal (azimuthal)
^^^^^^^^^^^^^^^^^^^^

.. asdf-autoschemas::

   transform/airy-1.2.0
   transform/gnomonic-1.2.0
   transform/slant_orthographic-1.2.0
   transform/slant_zenithal_perspective-1.2.0
   transform/stereographic-1.2.0
   transform/zenithal_equal_area-1.2.0
   transform/zenithal_equidistant-1.2.0
   transform/zenithal_perspective-1.3.0
