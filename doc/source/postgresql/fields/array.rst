ArrayField
==========

This is a field that represents native postgresql array. It can be of type integer and type text, but not limited to these.

Types supported:
^^^^^^^^^^^^^^^^

- **int** (int[])
- **text** (text[])
- **double precision** (double precision[])
- **real** (real[])
- **varchar(N)** (varchar(N)[])

Usage in model declaration:
---------------------------

.. code-block:: python

    from django.db import models
    from django_orm.postgresql.fields.arrays import ArrayField
    from django_orm.postgresql.manager import PgManager

    class TestModel(models.Model):
        my_int_list = ArrayField(dbtype='int', null=True)
        my_text_list = ArrayField(dbtype='text', null=True)

        objects = PgManager()
    


Creating sample objects:
------------------------

.. code-block:: python

    >>> TestModel.objects.create(
    ...     my_int_list = [1,2,3,4],
    ...     my_text_list = ['Hello', 'World'],
    ...     my_varchar_list = ['foo', 'bar']
    ... )
    <TestModel: TestModel object>
    >>> TestModel.objects.create(
    ...     my_int_list = [5,6,7,8,9],
    ...     my_text_list = ['Goodbye', 'World'],
    ...     my_varchar_list = ['door', 'window']
    ... )


Generated SQL for this create sentences:

.. code-block:: sql
    
    INSERT INTO "testapp_testmodel" 
        ("my_int_list", "my_text_list", "my_varchar_list") 
        VALUES (
            ARRAY[1, 2, 3, 4], 
            ARRAY['Hello', 'World'], 
            ARRAY['foo', 'bar']
        ) 
        RETURNING "testapp_testmodel"."id";

    INSERT INTO "testapp_testmodel" 
        ("my_int_list", "my_text_list", "my_varchar_list") 
        VALUES (
            ARRAY[5, 6, 7, 8, 9], 
            ARRAY['Goodbye', 'World'], 
            ARRAY['door', 'window']
        ) 
        RETURNING "testapp_testmodel"."id"; 


Operations with arrays reference examples:
------------------------------------------

Array length:
"""""""""""""

.. code-block:: python

    >>> TestModel.objects.filter(id=2).array_length(attr="my_int_list")
    5

Generated SQL for this sentence:
    
.. code-block:: sql
    
    SELECT (array_length(my_int_list, 1)) AS "_" 
        FROM "testapp_testmodel" WHERE "testapp_testmodel"."id" = 2;


Array slice:
""""""""""""

.. code-block:: python

    >>> TestModel.objects.filter(id=2).array_slice("my_int_list", 1, 3)
    [6, 7, 8]


Generated SQL for this sentence:

.. code-block:: sql

    SELECT (my_int_list[2:4]) AS "_" 
        FROM "testapp_testmodel" WHERE "testapp_testmodel"."id" = 2;


Aggregates for arrays:
----------------------

Array length annotate:
""""""""""""""""""""""

.. code-block:: python 

    >>> from django_orm.postgresql.aggregates import ArrayLength
    >>> for item in TestModel.objects.annotate(lista_length=ArrayLength('my_int_list')):
    ...     print item.id, item.my_int_list, item.lista_length
    ... 
    1 [1, 2, 3, 4] 4.0
    2 [5, 6, 7, 8, 9] 5.0

Generated SQL for this sentence:

.. code-block:: sql

    SELECT 
        "testapp_testmodel"."id", 
        "testapp_testmodel"."my_int_list", 
        "testapp_testmodel"."my_text_list", 
        array_length("testapp_testmodel"."my_int_list", 1) AS "lista_length" 
    FROM "testapp_testmodel" 
        GROUP BY 
            "testapp_testmodel"."id", 
            "testapp_testmodel"."my_int_list", 
            "testapp_testmodel"."my_text_list";


Array length aggregate:
"""""""""""""""""""""""

.. code-block:: python

    >>> TestModel.objects.aggregate(sum_of_all_lengths=ArrayLength('my_int_list', sum=True))
    {'sum_of_all_lengths': 9.0}


Generated SQL for this sentence:

.. code-block:: sql
    
    SELECT sum(array_length("testapp_testmodel"."my_int_list", 1)) AS "sum_of_all_lengths" 
        FROM "testapp_testmodel";


Query reference examples:
-------------------------

Simple querys:
""""""""""""""

.. code-block:: python
    
    >>> TestModel.objects.filter(my_int_list=[1,2,3,4])
    [<TestModel: TestModel object>]
    >>> TestModel.objects.filter(my_int_list__gt=[1,2,3,4])
    [<TestModel: TestModel object>]
    >>> TestModel.objects.filter(my_int_list__lt=[1,2,3,4])
    []


Generated SQL for this querys:

.. code-block:: sql

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" = ARRAY[1, 2, 3, 4] LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" > ARRAY[1, 2, 3, 4] LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" < ARRAY[1, 2, 3, 4]  LIMIT 21;


IndexExact Query:
"""""""""""""""""

.. code-block:: python

    >>> TestModel.objects.filter(my_int_list__indexexact=(0,1))
    [<TestModel: TestModel object=1>]
    >>> TestModel.objects.filter(my_int_list__indexexact=(0,5))
    [<TestModel: TestModel object=2>]
    >>> TestModel.objects.filter(my_int_list__indexexact=(0,6))
    []


Generated SQL for this querys:

.. code-block:: sql

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list"[1] = 1 LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list"[1] = 5 LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list"
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list"[1] = 6 LIMIT 21;


Distinct Query:
"""""""""""""""

.. code-block:: python
    
    >>> TestModel.objects.filter(my_text_list__distinct=['Hello', 'World'])
    [<TestModel: TestModel object=2>]


Generated SQL for this querys:

.. code-block:: sql

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_text_list" <> ARRAY['Hello', 'World'] LIMIT 21;


Contains Query:
"""""""""""""""

.. code-block:: python

    >>> TestModel.objects.filter(my_int_list__contains=[1,2,3])
    [<TestModel: TestModel object=1>]
    >>> TestModel.objects.filter(my_int_list__contains=[1,2,4])
    [<TestModel: TestModel object=1>]
    >>> TestModel.objects.filter(my_int_list__contains=[1,2,8])
    []
    >>> TestModel.objects.filter(my_int_list__contains=1)
    [<TestModel: TestModel object=1>]


Generated SQL for this querys:

.. code-block:: sql

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" @> ARRAY[1, 2, 3] LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" @> ARRAY[1, 2, 4] LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" @> ARRAY[1, 2, 8] LIMIT 21;

    SELECT "niwi_testmodel"."id", "niwi_testmodel"."my_int_list", "niwi_testmodel"."my_text_list" 
        FROM "niwi_testmodel" 
        WHERE 1 = ANY("niwi_testmodel"."my_int_list") LIMIT 21;


Overlap Query:
""""""""""""""

.. code-block:: python

    >>> TestModel.objects.filter(my_int_list__overlap=[1,2,8])
    [<TestModel: TestModel object=1>, <TestModel: TestModel object=2>]
    >>> TestModel.objects.filter(my_int_list__overlap=[22,33])
    []


Generated SQL for this querys:

.. code-block:: sql

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" && ARRAY[1, 2, 8] LIMIT 21;

    SELECT "testapp_testmodel"."id", "testapp_testmodel"."my_int_list", "testapp_testmodel"."my_text_list" 
        FROM "testapp_testmodel" 
        WHERE "testapp_testmodel"."my_int_list" && ARRAY[22, 33] LIMIT 21;
