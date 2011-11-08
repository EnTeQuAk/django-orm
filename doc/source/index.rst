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

Summary of characteristics (current and future)
-----------------------------------------------

Supported backends with connection pooling:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* PostgreSQL 9.x: ``django_orm.backends.postgresql_psycopg2``
* MySQL 5.1: ``django_orm.backends.mysql``
* SQLite: ``django_orm.backends.sqlite3``


Generic features (All backends):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1
    
   orm-pool.rst
   orm-indexes.rst
   orm-f-expression.rst
   orm-unaccent-lookup.rst
   orm-cache.rst
   orm-objectlock.rst


..  PostgreSQL specific features:
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * HStore
    * Full Text Search
    * Unaccent
    * Server side cursors
    * Native types with full query lookups:
    * Arrays
    * Intervals
    * Bytea
    * Geometric


Database specific documentation index:
--------------------------------------

.. toctree::
   :maxdepth: 1

   mysql.rst
   sqlite.rst
   postgresql/index.rst
