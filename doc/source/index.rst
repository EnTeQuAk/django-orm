django-orm
==========

This small project consists in maintaining a backend for django-orm, with several enhancements that will be explained below.

Due to that there are lots of different "plugins" to use different parts of databases are not covered by the standard orm. 
In reality this is not the problem! The problem arises when you need to use multiple orm plugins at once, and that's where 
you can not import and use!

My main motivation in creating this project is to see to unify several "plugins" in one package, so it can be used 
independently if you want one or more of them.

I certainly do not want to take all the credit, because not all the work I have done, however if you'll take care of having 
a single integrated package with a stable api and covers the most popular databases: postgresql, mysql and sqlite3.

This is an evolution of the project **django-postgresql**. So do not limit myself to a single database and applied some 
improvements to all backends.

**NOTE**: Currently only suports the postgresql backend: ``django_orm.backends.postgresql_psycopg2``.

Summary of characteristics (current and future)
-----------------------------------------------

Supported backends:
^^^^^^^^^^^^^^^^^^^

* PostgreSQL 9.x: ``django_orm.backends.postgresql_psycopg2``
* MySQL 5.1 (in development): ``django_orm.backends.mysql``
* SQLite (in development): ``django_orm.backends.sqlite3``

Generic features:
^^^^^^^^^^^^^^^^^

* Connection Pool.
* Low level orm cache (not implemented)
* Object level lock (not implemented)
* Own statements of indices for the model (in development)

PostgreSQL specific features:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* HStore
* Full Text Search
* Unaccent
* Server side cursors
* Native types with full query lookups:

  - Arrays
  - Intervals
  - Bytea
  - Geometric (box, line, path, polygon, point, circle)


Table of Contents:
------------------

.. toctree::
   :maxdepth: 1
    
   orm-pool.rst
   orm-cache.rst
   orm-indexes.rst


Database specific documentation:
--------------------------------

.. toctree::
   :maxdepth: 1

   mysql.rst
   sqlite.rst
   postgresql/index.rst

.. Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

