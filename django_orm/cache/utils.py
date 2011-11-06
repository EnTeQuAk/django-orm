# -*- coding: utf-8 -*-

from django.conf import settings
CACHE_KEY_PREFIX = getattr(settings, 'ORM_CACHE_KEY_PREFIX', 'orm.cache')
CACHE_ALIAS = getattr(settings, 'ORM_CACHE_ALIAS', 'default')

def get_cache_key_for_pk(model, pk, **kwargs):
    current_key = '%s:%s' % (model._meta.db_table, pk)
    if kwargs:
        current_key += ":%s" % (":".join(["%s=%s" % (k,v) for k,v in kwargs.iteritems()]))
    return CACHE_KEY_PREFIX + ":" + current_key


def get_cache():
    from django.core.cache import get_cache as gcache
    return gcache(CACHE_ALIAS)
