Connection pool
===============

Django by default, does not incorporate any mechanism to reuse the connections to the 
database, and that in many cases is usually the bottleneck. Especially when the 
database is on a separate server.

In the backend, incorporates 2 types of pooled connections: QueuePool 
and PersistentPool (default).

**New**: Now supports backends: postgresql_psycopg2, mysql and sqlite3.

Classes:
^^^^^^^^

* **PersistentPool** → Maintains a connection for thread.
* **QueuePool** → Maintains a simple queue of connections, 
    and are handing out as they are used. Connections are created on demand.


Configuration example:
^^^^^^^^^^^^^^^^^^^^^^

This step is very simple, just using this backend is already using the pool of connections. 
Just need to configure the maximum connections that can be kept in memory (optional and 
only for QueuePool, default 10).

.. code-block:: python
    
    from django_orm import POOLTYPE_QUEUE

    DATABASES = {
        'default': {
            'ENGINE': 'django_orm.backends.postgresql_psycopg2',
            'NAME': 'niwiweb',
            'USER': 'niwi',
            'PASSWORD': '123123',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'OPTIONS': {
                'POOLSIZE': 5, # default is 10
                'POOLTYPE': POOLTYPE_QUEUE,
            }
        },
    }
