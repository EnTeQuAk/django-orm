# -*- coding: utf-8 -*-

from psycopg2.extras import register_hstore
from psycopg2.pool import ThreadedConnectionPool, PersistentConnectionPool

from django import VERSION
from django.db.backends.util import truncate_name
from django.db.backends.postgresql_psycopg2.base import CursorWrapper
from django.db.backends.postgresql_psycopg2.base import connection_created
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper
from django.db.backends.util import truncate_name

from django.core import signals
from django.conf import settings

from django_orm.backends.postgresql_psycopg2.creation import DatabaseCreation
from django_orm.backends.postgresql_psycopg2.operations import DatabaseOperations

from django_orm.postgresql.pool import QueuePool, PersistentPool
from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE

import threading
import datetime
import logging
import uuid

pool = None
log = logging.getLogger(__name__)

def make_connection_params(self, settings_dict):
    if settings_dict['NAME'] == '':
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("You need to specify NAME in your"
                                   " Django settings file.")
    conn_params = {
        'database': settings_dict['NAME'],
    }
    conn_params.update(settings_dict['OPTIONS'])
    if 'autocommit' in conn_params:
        del conn_params['autocommit']

    if settings_dict['USER']:
        conn_params['user'] = settings_dict['USER']
    if settings_dict['PASSWORD']:
        conn_params['password'] = settings_dict['PASSWORD']
    if settings_dict['HOST']:
        conn_params['host'] = settings_dict['HOST']
    if settings_dict['PORT']:
        conn_params['port'] = settings_dict['PORT']
    return conn_params


class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Psycopg2 database backend that allows the use 
    of server side cursors and connection poolings
    support.

    Server side cursors usage
    -------------------------
    
    from django_postgresql import server_side_cursors

    qs = Model.objects.all()
    with server_side_cursors(qs, itersize=100):
        for item in qs.iterator():
            item.value

    It is very efficient with tables, with lots of 
    data, and to reduce large amounts of memory when 
    evaluating a QuerySet.


    Connection pool config
    ----------------------

    This step is very simple, just using this backend 
    is already using the pool of connections. Just need 
    to configure the maximum connections that can be
    kept in memory (optional).

    Example:

        DATABASES = {
            'default': {
                'ENGINE': 'django_postgresql.postgresql_psycopg2',
                'NAME': 'niwiweb',
                'USER': 'niwi',
                'PASSWORD': '123123',
                'HOST': '127.0.0.1',
                'PORT': '5432',
                'OPTIONS': {
                    'POOLSIZE': 5, # default is 10
                }
            }, 
        }
    
    """

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.server_side_cursors = False
        self.server_side_cursor_itersize = None
        self.creation = DatabaseCreation(self)
        self.ops = DatabaseOperations(self)

    def close(self):
        global pool
        if self.connection is None:
            return
        if not self.connection.closed:
            pool.putconn(self.connection)
        self.connection = None

    def _register(self):
        # bypass future registrations
        self._register = lambda: None

        self.creation.install_hstore_contrib()
        register_hstore(self.connection, globally=True, unicode=True)


    def _cursor(self):
        """
        Returns a unique server side cursor if they are enabled, 
        otherwise falls through to the default client side cursors.
        """
        new_connection, set_tz = False, False
        settings_dict = self.settings_dict
        options = self.settings_dict.get('OPTIONS', {})
        pool_type = options.get('POOLTYPE', POOLTYPE_PERSISTENT)
        global pool, connections
        
        if not pool:
            conn_params = make_connection_params(self, self.settings_dict)
            poolclass = PersistentPool \
                if pool_type == POOLTYPE_PERSISTENT else QueuePool
            pool = poolclass(conn_params, self.isolation_level,
                self.settings_dict)

        if not self.connection:
            newcon, self.connection = pool.getconn()
            if newcon:
                new_connection = True

        cursor = None
        if self.server_side_cursors:
            cursor = self.connection.cursor(name='cur%s' %\
                str(uuid.uuid4()).replace('-', ''))
            cursor.tzinfo_factory = None
            if self.server_side_cursor_itersize is not None:
                cursor.itersize = self.server_side_cursor_itersize
        else:
            cursor = self.connection.cursor()
            cursor.tzinfo_factory = None
            
        if new_connection:
            if hasattr(self, '_get_pg_version'):
                self._get_pg_version()
            connection_created.send(sender=self.__class__,
                            connection=self)
        # register hstore
        self._register()
        return CursorWrapper(cursor)

    def make_debug_cursor(self, cursor):
        return utils.CursorDebugWrapper(cursor, self)
    
    def _postgres_version(self):
        """
        Django 1.3 and django 1.4 compatibilyty method
        """
        if getattr(self, '_pg_version', None) is None:
            from django_postgresql.postgresql_psycopg2.version import get_version
            self._pg_version = self._pg_version = get_version(self.connection)
        return self._pg_version
    
    @property
    def pg_version(self):
        return self._postgres_version()
