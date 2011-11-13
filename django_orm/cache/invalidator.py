# -*- coding: utf-8 -*-

from django_orm.cache.utils import get_cache
from django_orm.cache.utils import get_cache_key_for_pk
import logging; log = logging.getLogger('orm.cache')

cache = get_cache()

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
