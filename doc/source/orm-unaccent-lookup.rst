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


In postgresql, to use the unaccent lookup, we must have the extension installed! 
Furthermore, once installed,  you have to do a fix, which will create indexes 
with the function (postgresql 9.1 example):

.. code-block:: sql
    
    CREATE EXTENSION unaccent;
    ALTER FUNCTION unaccent(text) IMMUTABLE;

The other option is to install an alternative version unaccented:

.. code-block:: sql

    CREATE OR REPLACE FUNCTION unaccent(text) RETURNS text AS $$ 
    DECLARE input_string text := $1; 
    BEGIN 
        input_string := translate(input_string, 'àáâäãåāăąÀÁÂÄÃÅĀĂĄ', 'aaaaaaaaaaaaaaaaaa'); 
        input_string := translate(input_string, 'èéêëēĕėęěÈÉÊËÊĒĔĖĘĚ', 'eeeeeeeeeeeeeeeeeee'); 
        input_string := translate(input_string, 'ìíîïĩīĭÌÍÎÏĨĪĬ', 'iiiiiiiiiiiiii'); 
        input_string := translate(input_string, 'òóôöõōŏőÒÓÔÖÕŌŎŐ', 'oooooooooooooooo'); 
        input_string := translate(input_string, 'ùúûüũūŭůÙÚÛÜŨŪŬŮ', 'uuuuuuuuuuuuuuuu'); 
        input_string := translate(input_string, 'ñÑçÇ', 'nncc'); 
        return input_string; 
    END; $$ LANGUAGE plpgsql IMMUTABLE;
