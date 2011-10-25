# -*- coding: utf-8 -*-

from django import VERSION
from django.db.backends.util import truncate_name
from django.db.backends.mysql.base import CursorWrapper
from django.db.backends.mysql.base import connection_created, django_conversions
from django.db.backends.mysql.base import DatabaseWrapper as BaseDatabaseWrapper
from django.db.backends.util import truncate_name

from django.core import signals
from django.conf import settings

from django_orm.mysql.pool import QueuePool, PersistentPool
from django_orm import POOLTYPE_PERSISTENT, POOLTYPE_QUEUE

import threading
import datetime
import logging
import uuid

pool = None
log = logging.getLogger(__name__)

from MySQLdb.constants import CLIENT

def make_connection_params(self, settings_dict):
    if settings_dict['NAME'] == '':
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("You need to specify NAME in your"
                                   " Django settings file.")
    kwargs = {
        'conv': django_conversions,
        'charset': 'utf8',
        'use_unicode': True,
    }
    if settings_dict['USER']:
        kwargs['user'] = settings_dict['USER']
    if settings_dict['NAME']:
        kwargs['db'] = settings_dict['NAME']
    if settings_dict['PASSWORD']:
        kwargs['passwd'] = settings_dict['PASSWORD']
    if settings_dict['HOST'].startswith('/'):
        kwargs['unix_socket'] = settings_dict['HOST']
    elif settings_dict['HOST']:
        kwargs['host'] = settings_dict['HOST']
    if settings_dict['PORT']:
        kwargs['port'] = int(settings_dict['PORT'])
    
    # We need the number of potentially affected rows after an
    # "UPDATE", not the number of changed rows.
    kwargs['client_flag'] = CLIENT.FOUND_ROWS
    kwargs.update(settings_dict['OPTIONS'])
    return kwargs


class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Mysql database backend with connection poolings
    support.

    Connection pool config
    ----------------------

    This step is very simple, just using this backend 
    is already using the pool of connections. Just need 
    to configure the maximum connections that can be
    kept in memory (optional).

    Example:

        DATABASES = {
            'default': {
                'ENGINE': 'django_orm.backends.mysql',
                'NAME': 'niwiweb',
                'USER': 'niwi',
                'PASSWORD': '123123',
                'HOST': '127.0.0.1',
                'PORT': '',
                'OPTIONS': {
                    'POOLSIZE': 5, # default is 10
                }
            }, 
        }
    
    """

    def close(self):
        global pool
        if self.connection is None:
            return
        if not self.connection.closed:
            pool.putconn(self.connection)
        self.connection = None

    def _cursor(self):
        """
        Returns a unique server side cursor if they are enabled, 
        otherwise falls through to the default client side cursors.
        """
        new_connection, set_tz = False, False
        settings_dict = self.settings_dict
        options = self.settings_dict.get('OPTIONS', {})
        pool_type = options.get('POOLTYPE', POOLTYPE_PERSISTENT)

        global pool
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

        if new_connection:
            connection_created.send(sender=self.__class__,
                            connection=self)
        return CursorWrapper(cursor)
