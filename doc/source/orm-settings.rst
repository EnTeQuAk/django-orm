===========================
Database settings reference
===========================


Pool
----

* ``POOLSIZE``: (int) set max pool size. Only for QueuePool.
* ``POOLTYPE``: (enum) set a type of pool.
    | Values: django_orm.POOLTYPE_QUEUE, django_orm.POOLTYPE_PERSISTENT
    | Default: django_orm.POOLTYPE_PERSISTENT
* ``POOL_ENABLED``: (bool) set flat for enable connection pool.
    | Default: True
