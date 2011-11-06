# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings

from django_orm.cache.utils import get_cache
from django_orm.manager import Manager

import logging; log = logging.getLogger('orm.cache')

DEFAULT_CACHE_TIMEOUT = getattr(settings, 'ORM_CACHE_DEFAULT_TIMEOUT', 60)
DEFAULT_CACHE_ENABLED = getattr(settings, 'ORM_CACHE_DEFAULT_ENABLED', False)

cache = get_cache()

def ensure_default_manager(sender, **kwargs):
    options = getattr(sender, '_options', None)
    options_are_none  = False
    options_add_manager = False
    options_manager_name = 'objects'

    if options is None:
        options = {}
        options_are_none = True

    if "manager" in options:
        if options["manager"]:
            options_add_manager = True
            if isinstance(options['manager'], (str, unicode)):
                options_manager_name = options['manager']
    else:
        options['manager'] = False

    if not options_add_manager:
        log.info("Skiping model setting %s", sender.__name__)
        return
    else:
        log.info("Enabled manger on model %s", sender.__name__)

    sender.add_to_class('objects', Manager()) 

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
    
    if options_are_none:
        setattr(sender, '_options', options)

signals.class_prepared.connect(ensure_default_manager)

def invalidate_object(instance, **kwargs):
    cache.delete(instance.cache_key)
    log.info("Invalidating: %s(%s)", instance.__class__.__name__,
        instance.id)
