# -*- coding: utf-8 -*-

from django.db.backends.sqlite3.base import DatabaseWrapper as BaseDatabaseWrapper
from django_orm.pool import QueuePool, PersistentPool
from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE

pool = None

class DatabaseWrapper(BaseDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        options = self.settings_dict.get('OPTIONS', {})
        self.pool_type = options.get('POOLTYPE', POOLTYPE_PERSISTENT)
        self.pool_enabled = options.pop('POOL_ENABLED', True)

    def close(self):
        global pool

        if self.connection is None:
            return 

        print "Pool enabled: %s Connection closing: %s" % \
            (self.pool_enabled, id(self.connection))

        if not self.pool_enabled and self.settings_dict['NAME'] != ":memory:":
            BaseDatabaseWrapper.close(self)
            return

        pool.putconn(self.connection)
        self.connection = None

    def _cursor(self):
        global pool
        if not pool:
            poolclass = PersistentPool \
                if self.pool_type == POOLTYPE_PERSISTENT else QueuePool
            pool = poolclass(self.settings_dict)

        if self.connection is None:
            self.connection = pool.getconn()

        return super(DatabaseWrapper, self)._cursor()
