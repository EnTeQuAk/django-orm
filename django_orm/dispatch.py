# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings

import logging; log = logging.getLogger('orm.cache')

DEFAULT_CACHE_TIMEOUT = getattr(settings, 'ORM_CACHE_DEFAULT_TIMEOUT', 60)
DEFAULT_CACHE_ENABLED = getattr(settings, 'ORM_CACHE_DEFAULT_ENABLED', False)

class OrmMeta(object):
    options = {
        'cache_object': DEFAULT_CACHE_ENABLED,
        'cache_queryset': DEFAULT_CACHE_ENABLED,
        'default_timeout': DEFAULT_CACHE_TIMEOUT,
    }

def ensure_default_manager(sender, **kwargs):
    from django_orm.cache.utils import get_cache_key_for_pk
    from django_orm.cache.invalidator import invalidate_object
    from django_orm.manager import FTSManager as Manager
    from django.db import models

    meta_orm_class = getattr(sender, 'OrmMeta', None)
    if not meta_orm_class:
        meta_orm_obj = OrmMeta()
    else:
        meta_orm_obj = meta_orm_class()
        options = getattr(meta_orm_obj, 'options', {})

        if 'cache_object' not in options:
            options['cache_object'] = DEFAULT_CACHE_ENABLED
        
        if 'cache_queryset' not in options:
            options['cache_queryset'] = DEFAULT_CACHE_ENABLED
        
        if options['cache_queryset']:
            options['cache_object'] = True

        if 'default_timeout' not in options:
            options['default_timeout'] = DEFAULT_CACHE_TIMEOUT

        meta_orm_obj.options = options
    
    sender.add_to_class('_orm_meta', meta_orm_obj)
    if not getattr(sender, '_orm_manager', None):
        sender.add_to_class('_orm_manager', Manager())

    sender.add_to_class('_get_cache_key_for_pk', 
        staticmethod(lambda x,y: get_cache_key_for_pk(x, y)))
    sender.add_to_class('cache_key', 
        property(lambda x: x._get_cache_key_for_pk(x.__class__, x.pk)))

signals.class_prepared.connect(ensure_default_manager)
