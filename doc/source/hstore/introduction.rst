HStore introduction
===================

Limitations and notes
---------------------

- Due to how Django implements its ORM, you will need to use the custom ``postgresql_psycopg2`` backend
  defined in this package, which naturally will prevent you from dropping in other django extensions
  which require a custom backend (unless you fork and combine).
  Within my means, I will look to integrate into this package, interesting extensions. The proposals are always welcome.
- PostgreSQL's implementation of hstore has no concept of type; it stores a mapping of string keys to
  string values. This library makes no attempt to coerce keys or values to strings.


Note to postgresql 9.0 users: 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If using postgresql9.0 must manually install the extension hstore to create the database 
or make hstore already installed in the corresponding template. For an example, you can see the file "runtests-pg90".

Note to South users:
^^^^^^^^^^^^^^^^^^^^

If you keep getting errors like `There is no South database module 'south.db.None' for your database.`, add the following to `settings.py`:

.. code-block:: python

    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}


Classes
-------

The library provides three principal classes:

``django_postgresql.hstore.DictionaryField``
    An ORM field which stores a mapping of string key/value pairs in an hstore column.
``django_postgresql.hstore.ReferencesField``
    An ORM field which builds on DictionaryField to store a mapping of string keys to
    django object references, much like ForeignKey.
``django_postgresql.hstore.HStoreManager``
    An ORM manager which provides much of the query functionality of the library.


Example of model declaration:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.db import models
    from django_postgresql import hstore

    class Something(models.Model):
        name = models.CharField(max_length=32)
        data = hstore.DictionaryField(db_index=True)
        objects = hstore.HStoreManager()

        def __unicode__(self):
            return self.name


You then treat the ``data`` field as simply a dictionary of string pairs:

.. code-block:: python

    instance = Something.objects.create(name='something', data={'a': '1', 'b': '2'})
    assert instance.data['a'] == '1'

    empty = Something.objects.create(name='empty')
    assert empty.data == {}

    empty.data['a'] = '1'
    empty.save()
    assert Something.objects.get(name='something').data['a'] == '1'


You can issue indexed queries against hstore fields:

.. code-block:: python

    # equivalence
    Something.objects.filter(data={'a': '1', 'b': '2'})

    # subset by key/value mapping
    Something.objects.filter(data__contains={'a': '1'})

    # subset by list of keys
    Something.objects.filter(data__contains=['a', 'b'])

    # subset by single key
    Something.objects.filter(data__contains='a')


You can also take advantage of some db-side functionality by using the manager:

.. code-block:: python

    # identify the keys present in an hstore field
    >>> Something.objects.hkeys(id=instance.id, attr='data')
    ['a', 'b']

    # peek at a a named value within an hstore field
    >>> Something.objects.hpeek(id=instance.id, attr='data', key='a')
    '1'

    # do the same, after filter
    >>> Something.objects.filter(id=instance.id).hpeek(attr='data', key='a')
    '1'

    # remove a key/value pair from an hstore field
    >>> Something.objects.filter(name='something').hremove('data', 'b')


The hstore methods on manager pass all keyword arguments aside from ``attr`` and ``key``
to ``.filter()``.

