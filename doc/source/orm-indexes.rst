Own statements of indixes for a model
=====================================

It allows a simple way to add more additional indices to a particular model.

Supported backends: 

* ``django_orm.backends.postgresql_psycopg2``
* ``django_orm.backends.mysql``
* ``django_orm.backends.sqlite3``

How it works:
^^^^^^^^^^^^^

It is very simple, add the attribute ``indexes`` with a list of custom indices to ``OrmMeta`` class defined
on a model.

Example:

.. code-block:: python

    class Person(models.Model):
        name = models.CharField(max_length=200)

        class OrmMeta:
            indexes = [
                'CREATE INDEX person_name_idx0 ON pages USING BTREE (lower(name));',
                'CREATE INDEX person_name_idx1 ON pages USING BTREE (lower(name) varchar_pattern_ops);',
            ]
