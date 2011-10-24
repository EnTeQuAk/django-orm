PostgreSQL Aggregates
=====================

Unaccent (Contrib)
------------------

It is an aggregation function that admits any field of type "CharField" or "TextField" and leaves without accents.

Usage example:

.. code-block:: python

    >>> from niwi.models import Post
    >>> from django_orm.postgresql.aggregates import Unaccent
    >>> qs = Post.objects.annotate(title_unaccent=Unaccent('title')).filter(pk=15)
    >>> print qs[0].title
    Tipado estático en python.
    >>> print qs[0].title_unaccent
    Tipado estatico en python.

Note for postgresql9.0 users:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use this feature, you must install the extension unaccented. 

Example::
    
    psql -U user dbname -f /usr/share/postgresql/contrib/unaccent.sql


Note for postgresql9.1 users:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use this feature, you must install the extension unaccented.

Example::
    
    psql -U user dbname -c "CREATE EXTENSION unaccent;" -q
