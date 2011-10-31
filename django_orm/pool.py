# -*- coding: utf-8 -*-

from Queue import Queue
import threading

from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE

class PoolError(Exception):
    pass

class QueuePool(object):
    """ 
    Psycopg2-Django ORM Queue connection pool implementation.
    """

    def __init__(self, settings):
        options = settings.get('OPTIONS', {})
        self.maxconn = "POOLSIZE" in options \
            and int(options['POOLSIZE']) or 10
        self._pool = Queue()

    def _getconn(self):
        """
        Internal method: get connection from
        pool or create one new connection.
        """
        if self._pool.qsize() == 0:
            return None
        try:
            return self._pool.get(block=False)
        except Queue.Empty:
            return None

    def _putconn(self, conn):
        """
        Internal method: put connection into a pool
        if this not full else, close connection.
        """
        if self._pool.qsize() >= self.maxconn:
            conn.close()
        else:
            self._pool.put(conn, block=False)

        #print "Pool debug: size:",  self._pool.qsize()

    def getconn(self):
        """
        Public method for get connection 
        from a pool.
        """
        return self._getconn()

    def putconn(self, conn):
        """
        Public method for put connection
        into a pool.
        """
        self._putconn(conn)


thr_local = threading.local()

class PersistentPool(QueuePool):
    """
    Thread persistent connection pool.

    QueuePool is similar to, but maintains 
    a queue for each thread, thus ensuring 
    that a thread always receives the same 
    connections.

    In most of my tests with django, only one 
    connection is maintained by thread.
    """
    def _getconn(self):
        if hasattr(thr_local, 'connection') and \
                thr_local.connection is not None:
            return thr_local.connection

        return None

    def _putconn(self, conn):
        if conn is not None:
            conn.commit()
        thr_local.connection = conn
