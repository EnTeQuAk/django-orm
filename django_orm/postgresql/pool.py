# -*- coding: utf-8 -*-

from Queue import Queue
import threading
import psycopg2

from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE
from django_orm.basepool import BaseQueuePool, BasePersistentPool

class QueuePool(BaseQueuePool):
    """ 
    Psycopg2-Django ORM Queue connection pool implementation.
    """
    def _connect(self):
        """
        Method for make a new database connection
        and set correct timezone and client encoding..
        """
        conn = psycopg2.connect(**self.dbparams)
        conn.set_client_encoding('UTF8')
        conn.set_isolation_level(self._isolation_level)

        cursor = conn.cursor()
        cursor.execute("SET TIME ZONE %s", [self._settings['TIME_ZONE']])
        cursor.close()
        return conn

    def _try_connected(self, connection):
        """
        Try if connection object is connected
        to a database.

        :param psycopg.connection connection: db connection.
        :returns: True or False
        :rtype: bool
        """
        try:
            connection.cursor().execute("SELECT 1;")
            return True
        except psycopg2.OperationalError:
            return False


thr_local = threading.local()

class PersistentPool(BasePersistentPool):
    """
    Thread persistent connection pool.

    QueuePool is similar to, but maintains 
    a queue for each thread, thus ensuring 
    that a thread always receives the same 
    connections.

    In most of my tests with django, only one 
    connection is maintained by thread.
    """
    def _connect(self):
        """
        Method for make a new database connection
        and set correct timezone and client encoding..
        """
        conn = psycopg2.connect(**self.dbparams)
        conn.set_client_encoding('UTF8')
        conn.set_isolation_level(self._isolation_level)

        cursor = conn.cursor()
        cursor.execute("SET TIME ZONE %s", [self._settings['TIME_ZONE']])
        cursor.close()
        return conn

    def _try_connected(self, connection):
        """
        Try if connection object is connected
        to a database.

        :param psycopg.connection connection: db connection.
        :returns: True or False
        :rtype: bool
        """
        try:
            connection.cursor().execute("SELECT 1;")
            return True
        except psycopg2.OperationalError:
            return False
