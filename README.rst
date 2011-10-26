django_orm
==========

Advanced improvement to django orm with third-party modules in one with some usefull features.

**Docs:** http://readthedocs.org/docs/django-orm/en/latest/


Notice
======

Main motivation of this project is to unify what is done to django_postgresql and make it available, as far as is compatible with mysql and sqlite. And besides, add things specific to each database.

**The future of the project django-postgresql continue on this project.**


TODO (in development):
----------------------

* ORM low level cache for all backends.
* Some advanced features of mysql (suggestions welcome)
* Lock system for objects on all backends.

Requirements:
-------------

* PostgreSQL >= 9.0 (if use postgresql_psycopg2 backend)
* Psycopg2 >= 2.4 (if use postgresql_psycopg2 backend)
* MySQLdb (if use mysql backend)
* Django >= 1.3
* Sqlite3

Features:
---------

* PostgreSQL server side cursors.
* PostgreSQL hstore integration.
* PostgreSQL unaccent aggregation.
* PostgreSQL Full Text Search.
* Builtin connection pool. (PostgreSQL, MySQL, Sqlite3)
* Additional indexes creation method from model. (PostgreSQL, MySQL, Sqlite3)

