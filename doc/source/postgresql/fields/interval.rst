=============
IntervalField
=============

It is a wrapper for an interval type field of postgresql. And to store and work with time intervals. 
In python, to represent this data is used :py:class:`~datetime.timedelta`.

**Supported lookups on querysets:**

- gt
- gte
- lt
- lte
- exact

--------------------------
Example model declaration:
--------------------------

This is a simple example of a model that contains this field.

.. code-block:: python

    from django.db import models
    from django_orm.postgresql.fields.interval import IntervalField
    from django_orm.manager import Manager

    class TestModel(models.Model):
        iv = IntervalField()
        objects = Manager()


------------------------
Creating sample objects:
------------------------

To teach how to use this field, and what kind of queries can be done with, we create sample data.

.. code-block:: python

    from datetime import timedelta
    TestModel.objects.create(iv=timedelta(20))
    TestModel.objects.create(iv=timedelta(34, 55))


Generated SQL for this create sentences:

.. code-block:: sql

    INSERT INTO "niwi_testmodel" ("iv") 
        VALUES ('20 days 0.000000 seconds'::interval) 
        RETURNING "niwi_testmodel"."id";

    INSERT INTO "niwi_testmodel" ("iv") 
        VALUES ('34 days 55.000000 seconds'::interval) 
        RETURNING "niwi_testmodel"."id";


-------------------------
Query reference examples:
-------------------------

Simple exact ang gt lookup querys:

.. code-block:: python
   
    >>> TestModel.objects.filter(iv__gt=timedelta(21))
    [<TestModel: TestModel object=5>]
    >>> TestModel.objects.filter(iv=timedelta(20))
    [<TestModel: TestModel object=4>]


Generated SQL for this sentences:

.. code-block:: sql

    SELECT "niwi_testmodel"."id", "niwi_testmodel"."iv" 
        FROM "niwi_testmodel" 
        WHERE "niwi_testmodel"."iv" > '21 days 0.000000 seconds'::interval  
        LIMIT 21;
    
    SELECT "niwi_testmodel"."id", "niwi_testmodel"."iv" 
        FROM "niwi_testmodel" 
        WHERE "niwi_testmodel"."iv" = '20 days 0.000000 seconds'::interval  
        LIMIT 21;


------------------
Bulk update querys
------------------

The method F () which gives us django, and allows us to update a field using the 
value of another field rather than a constant. This method also can be used to IntervalField.

.. code-block:: python

    >>> TestModel.objects.filter(id=5).update(iv=F('iv') + timedelta(26))
    1
    >>> TestModel.objects.filter(id=5).update(iv=F('iv') - timedelta(26))
    1

Generated SQL for this sentences:

.. code-block:: sql
    
    UPDATE "niwi_testmodel" 
        SET "iv" = ("niwi_testmodel"."iv" + interval '26 days') 
        WHERE "niwi_testmodel"."id" = 5;

    UPDATE "niwi_testmodel" 
        SET "iv" = ("niwi_testmodel"."iv" - interval '26 days') 
        WHERE "niwi_testmodel"."id" = 5;

