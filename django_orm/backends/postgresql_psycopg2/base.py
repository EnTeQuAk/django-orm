# -*- coding: utf-8 -*-

from psycopg2.extras import register_hstore
from psycopg2.pool import ThreadedConnectionPool, PersistentConnectionPool

from django import VERSION
from django.db.backends.postgresql_psycopg2.base import connection_created, CursorWrapper
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper
from django.db.backends.util import truncate_name

from django.core import signals
from django.conf import settings

from django_orm.backends.postgresql_psycopg2.creation import DatabaseCreation
from django_orm.backends.postgresql_psycopg2.operations import DatabaseOperations

from django_orm.pool import QueuePool, PersistentPool
from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE

import threading
import datetime
import logging
import uuid

pool = None
log = logging.getLogger(__name__)

class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Psycopg2 database backend that allows the use 
    of server side cursors and connection poolings
    support.
    """
    _pg_version = None

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.server_side_cursors = False
        self.server_side_cursor_itersize = None
        self.ops = DatabaseOperations(self)
        self.creation = DatabaseCreation(self)

    def _try_connected(self):
        """
        Try if connection object is connected
        to a database.

        :param psycopg.connection connection: db connection.
        :returns: True or False
        :rtype: bool
        """
        try:
            self.connection.cursor().execute("SELECT 1;")
            return True
        except psycopg2.OperationalError:
            return False

    def close(self):
        global pool
        if self.connection is None:
            return
        
        print "Connection closing:", id(self.connection)
        if not self.connection.closed:
            #self.connection.close()
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
        global pool
        settings_dict = self.settings_dict
        options = self.settings_dict.get('OPTIONS', {})
        pool_type = options.get('POOLTYPE', POOLTYPE_PERSISTENT)

        if not pool:
            poolclass = PersistentPool \
                if pool_type == POOLTYPE_PERSISTENT else QueuePool
            pool = poolclass(self.settings_dict)
        
        if self.connection is None:
            self.connection = pool.getconn()
            if self.connection is not None and not self._try_connected():
                self.connection.close()
                self.connection = None

        cursor = super(DatabaseWrapper, self)._cursor()
        if self.server_side_cursors:
            cursor = self.connection.cursor(name='cur%s' %\
                str(uuid.uuid4()).replace('-', ''))
            cursor.tzinfo_factory = None
            if self.server_side_cursor_itersize is not None:
                cursor.itersize = self.server_side_cursor_itersize
            cursor = CursorWrapper(cursor)

        if not hasattr(self, '_version'):
            try:
                from django.db.backends.postgresql.version import get_version
                self.__class__._version = get_version(cursor)
            except ImportError:
                pass

        if self._pg_version is None:
            try:
                from django_postgresql.postgresql_psycopg2.version import get_version
                self._pg_version = get_version(self.connection)
            except ImportError:
                pass
        return cursor


from django.dispatch import receiver

@receiver(connection_created)
def my_callback(sender, connection, signal, **kwargs):
    print "Connection created:", id(connection.connection)
