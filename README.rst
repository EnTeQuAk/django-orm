django_orm
==========

Advanced improvement to django orm with third-party modules in one with some usefull features:

 * connection pool
 * postgresql server-sider cursors
 * postgresql native complex types
 * postgresql hstore and unaccent.


* **Documentation for postgresql:** http://readthedocs.org/docs/django-postgresql/en/latest/

Notice
======

Main motivation of this project is to unify what is done to django_postgresql and make it available, as far as is compatible with mysql and sqlite. And besides, add things specific to each database.

The project development will be integrated django-postgresql in it.


Requirements:
-------------

* PostgreSQL >= 9.0 (if use postgresql_psycopg2 backend)
* Psycopg2 >= 2.4 (if use postgresql_psycopg2 backend)
* MySQLdb (if use mysql backend)
* Django >= 1.3

Features:
---------

* PostgreSQL server side cursors.
* PostgreSQL hstore integration.
* PostgreSQL unaccent aggregation.
* PostgreSQL Full Text Search.
* Builtin connection pool. (temporary only disponible to postgresql, mysql and sqlite work in progress)
