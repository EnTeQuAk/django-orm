Unaccent lookups for searches ignoring accents
==============================================

Unaccented lookup enables a simple and independent of the database, search type 'LIKE' or 
'ILIKE' but ignoring accents.

The 'models.CharField' by default does not support this lookup, for this reason, 'django-orm', 
has an own implementation of the field that allows this type of lookup.

Lookups:
^^^^^^^^

* ``unaccent``
* ``iunaccent``

**NOTE**: On mysql backend iunaccent is a sinonym of unaccent.

Examples:
^^^^^^^^^

This is an example of using this lookup:

.. code-block:: python
    
    >>> TestModel.objects.filter(name__unaccent='Andreó')
    [<TestModel: TestModel object>, <TestModel: TestModel object>]
    >>> TestModel.objects.filter(name__iunaccent='Andreó')
    [<TestModel: TestModel object>, <TestModel: TestModel object>]


Possible sql output (postgresql):

.. code-block:: sql

    SELECT "testmodel"."id", "testmodel"."name", "testmodel"."desc" 
        FROM "testmodel" WHERE unaccent("testmodel"."name") LIKE unaccent('%Andreó%') LIMIT 21;
    SELECT "testmodel"."id", "testmodel"."name", "testmodel"."desc" 
        FROM "testmodel" WHERE lower(unaccent("testmodel"."name")) LIKE lower(unaccent('%Andreó%')) LIMIT 21;
