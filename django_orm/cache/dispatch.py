# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings

from django_orm.cache.utils import get_cache
from django_orm.cache.utils import get_cache_key_for_pk

from django_orm.manager import Manager

import logging; log = logging.getLogger('orm.cache')

DEFAULT_CACHE_TIMEOUT = getattr(settings, 'ORM_CACHE_DEFAULT_TIMEOUT', 60)
DEFAULT_CACHE_ENABLED = getattr(settings, 'ORM_CACHE_DEFAULT_ENABLED', False)
DEFAULT_ADD_MANAGER = getattr(settings, 'ORM_CACHE_DEFAULT_ADD_MANAGER', True)
DEFAULT_MANAGER_ALIAS = getattr(settings, 'ORM_CACHE_DEFAULT_MANAGER_ALIAS', 'objects')
cache = get_cache()

def ensure_default_manager(sender, **kwargs):
    options = getattr(sender, '_options', {})
    options_are_none  = False
    options_add_manager = DEFAULT_ADD_MANAGER
    options_manager_name = DEFAULT_MANAGER_ALIAS

    if "manager" in options:
        if options["manager"]:
            if isinstance(options['manager'], (str, unicode)):
                options_manager_name = options['manager']
    else:
        options['manager'] = False
    
    if options['manager']:
        sender.add_to_class(options_manager_name, Manager())

    sender.add_to_class('_get_cache_key_for_pk', 
        staticmethod(lambda x,y: get_cache_key_for_pk(x, y)))
    sender.add_to_class('cache_key', 
        property(lambda x: x._get_cache_key_for_pk(x.__class__, x.pk)))

    if 'cache_object' not in options:
        options['cache_object'] = DEFAULT_CACHE_ENABLED
    
    if 'cache_queryset' not in options:
        options['cache_queryset'] = DEFAULT_CACHE_ENABLED
    
    if options['cache_queryset']:
        options['cache_object'] = True

    if 'default_timeout' not in options:
        options['default_timeout'] = DEFAULT_CACHE_TIMEOUT
    
    signals.post_save.connect(invalidate_object, sender=sender)
    signals.post_delete.connect(invalidate_object, sender=sender)
    #sender._options = options
    setattr(sender, '_options', options)


signals.class_prepared.connect(ensure_default_manager)

def invalidate_object(instance, **kwargs):
    log.info("Invalidating: %s(%s)", instance.__class__.__name__,
        instance.id)
    cache.delete(instance.cache_key)
    if hasattr(cache, 'keys'):
        log.info("Searching querysets with this model...")
        find_pattern = "*qs:default:table:%s*" % \
            instance.__class__._meta.db_table
        keys = cache.keys(find_pattern)
        log.info("Found %s keys for querysets. Invalidating...", len(keys))
        log.info("Keys: %s", str(keys))
        cache.delete_many(keys)
    else:
        log.warning("Cache backend not suport keys method. "
            "Without this method is imposible invalidate querysets. "
            "This feature is disabled!")
