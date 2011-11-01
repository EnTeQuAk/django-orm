==========
ByteaField
==========

It is a wrapper for an bytea type field of postgresql. **Note**: this field is only for
store binary data, not allowed querys.

--------------------------
Example model declaration:
--------------------------

This is a simple example of a model that contains this field.

.. code-block:: python

    from django.db import models
    from django_orm.postgresql.fields.bytea import ByteaField
    from django_orm.manager import Manager

    class TestModel(models.Model):
        bb = ByteaField()
        objects = Manager()


------------------------
Creating sample objects:
------------------------

To teach how to use this field, and what kind of queries can be done with, we create sample data.

.. code-block:: python

    >>> bindata
    '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\xde'
    >>> TestModel.objects.create(bb=bindata)
    <TestModel: TestModel object=1>


Generated SQL for this create sentences:

.. code-block:: sql
    
    INSERT INTO "niwi_testmodel" ("bb") 
        VALUES ('\x89504e470d0a1a0a0000000d49484452000002de'::bytea) 
        RETURNING "niwi_testmodel"."id";
