.. _asdf-schema:

ASDF Schema
===========

.. toctree::
   :hidden:

   schemas/stsci.edu/asdf/asdf-schema-1.0.0.rst

:ref:`ASDF Schema <http://stsci.edu/schemas/asdf/asdf-schema-1.0.0>`
further extends YAML schema to add some validations specific to ASDF,
notably to do with :ref:`ndarray
<http://stsci.edu/schemas/asdf/core/ndarray-1.0.0>`.

``ndim`` keyword
^^^^^^^^^^^^^^^^

Specifies that the matching ndarray is exactly the given
number of dimensions.

``max_ndim`` keyword
^^^^^^^^^^^^^^^^^^^^

Specifies that the corresponding ndarray is at most the given number
of dimensions.  If the array has fewer dimensions, it should be
logically treated as if it were "broadcast" to the expected dimensions
by adding 1's to the front of the shape list.

``datatype`` keyword
^^^^^^^^^^^^^^^^^^^^

Specifies the datatype of the ndarray.

By default, an array is considered "matching" if the array can be cast
to the given datatype without data loss.  For exact datatype matching,
set ``exact_datatype`` to ``true``.

``exact_datatype`` keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^

If ``true``, the datatype must match exactly, rather than just being
castable to the given datatype without data loss.

