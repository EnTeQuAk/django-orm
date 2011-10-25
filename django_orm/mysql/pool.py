# -*- coding: utf-8 -*-

from Queue import Queue
import threading

import MySQLdb as Database

DatabaseError = Database.DatabaseError
IntegrityError = Database.IntegrityError

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
        from django.utils.safestring import SafeString, SafeUnicode

        conn = Database.connect(**self.dbparams)
        conn.encoders[SafeUnicode] = conn.encoders[unicode]
        conn.encoders[SafeString] = conn.encoders[str]
        
        cursor = conn.cursor()
        cursor.execute("SET SQL_AUTO_IS_NULL = 0")
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
            connection.ping()
            return True
        except DatabaseError:
            connection.close()
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
    pass
