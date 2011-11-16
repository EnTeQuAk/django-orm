django_orm
==========

Advanced improvement to django orm with third-party modules in one with some usefull features.

**Docs:** http://readthedocs.org/docs/django-orm/en/latest/

Global features:
----------------

* Builtin connection pool. (PostgreSQL, MySQL, Sqlite3)
* Additional indexes creation method from model. (PostgreSQL, MySQL, Sqlite3)
* ORM low level cache for all backends. (beta)
* Unaccent lookup for searches without accents.

Only PostgreSQL features:
-------------------------

* PostgreSQL Full Text Search.
* PostgreSQL complex types and full queryset lookups.
* PostgreSQL server side cursors.
* PostgreSQL hstore integration.
* PostgreSQL unaccent aggregation.

Requirements:
-------------

* PostgreSQL >= 9.0 (if use postgresql_psycopg2 backend)
* Psycopg2 >= 2.4 (if use postgresql_psycopg2 backend)
* MySQLdb (if use mysql backend)
* Django >= 1.3
* Sqlite3
