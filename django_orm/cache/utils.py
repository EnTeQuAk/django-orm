# -*- coding: utf-8 -*-

from django.conf import settings
CACHE_KEY_PREFIX = getattr(settings, 'ORM_CACHE_KEY_PREFIX', 'orm.cache')

def get_cache_key_for_pk(model, pk, **kwargs):
    current_key = '%s:%s' % (model._meta.db_table, pk)
    if kwargs:
        current_key += ":%s" % (":".join(["%s=%s" % (k,v) for k,v in kwargs.iteritems()]))
    return CACHE_KEY_PREFIX + ":" + current_key
