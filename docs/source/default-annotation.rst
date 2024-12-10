.. _default-annotation:

Default annotation
==================

The JSON Schema spec includes a schema annotation attribute called ``default`` that
can be used to describe the default value of a data attribute when that attribute
is missing.  Recent versions of the spec `point out <http://json-schema.org/draft/2019-09/json-schema-core.html#rfc.section.7.7.1.1>`__
that there is no single correct way to choose an annotation value when multiple
are available due to references and combiners.  This presents a problem when
trying to fill in missing data in a file based on the schema ``default``: if
multiple conflicting values are available, the software does not know how to choose.

Previous versions of the ASDF Standard did not offer guidance on how
to use ``default``.  The Python reference implementation read the first default
that it encountered as a literal value and inserted that value into the tree when
the corresponding attribute was otherwise missing.  Until version 2.8, it also
removed attributes on write whose values matched their schema defaults.  The
resulting files would appear to the casual viewer to be missing data, and may in
fact be invalid against their schemas if the any of the removed attributes were required.

Implementations **must not** remove attributes with default values from the tree.
Beginning with ASDF Standard 1.6.0, implementations also must not fill default values
directly from the schema.  This will avoid ambiguity when multiple schema defaults
are present, and also permit the ``default`` attribute to contain a description
that is not appropriate to use as a literal default value.  For example::

    default: An array of zeros matching the dimensions of the data array.

For ASDF Standard < 1.6.0, filling default values from the schema is required.  This is
necessary to support files written by older versions of the Python implementation.
