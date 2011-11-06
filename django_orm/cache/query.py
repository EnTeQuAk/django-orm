from django.db.models.query import QuerySet, ITER_CHUNK_SIZE
from django.db import backend, connection
from django.core.cache import cache
from django.conf import settings

from django_orm.cache.utils import get_cache_key_for_pk
from django_orm.cache.exceptions import CacheMissingWarning

CACHE_KEY_PREFIX = getattr(settings, 'ORM_CACHE_KEY_PREFIX', 'orm.cache')

import copy, hashlib
import logging; log = logging.getLogger('orm.cache')

class CachedQuerySetMixIn(object):
    from_cache = False
    cache_object_enable = False
    cache_queryset_enable = False

    def __init__(self, *args, **kwargs):
        self.cache_key_prefix = CACHE_KEY_PREFIX
        super(CachedQuerySetMixIn, self).__init__(*args, **kwargs)

        options = getattr(self.model, '_options')
        self.cache_object_enable = options['cache_object']
        self.cache_queryset_enable = options['cache_queryset']
        self.cache_timeout = options['default_timeout']

    def query_key(self):
        sql, params = self.query.get_compiler(using=self.db).as_sql()
        return "%s:queryset:%s:%s" % (
            CACHE_KEY_PREFIX,
            self.model.__name__,
            hashlib.sha1(sql % params).hexdigest()
        )

    def cache(self, timeout=None):
        if not timeout:
            timeout = self.cache_timeout

        qs = self._clone()
        qs.cache_object_enable = True
        qs.cache_queryset_enable = True
        qs.cache_timeout = timeout
        return qs

    def get(self, *args, **kwargs):
        if not self.cache_object_enable:
            return super(CachedQuerySetMixIn, self).get(*args, **kwargs)

        if len(args) > 0:
            return super(CachedQuerySetMixIn, self).get(*args, **kwargs)
        
        pk, params, obj = None, copy.deepcopy(kwargs), None
        if "pk" in params:
            pk = params.pop('pk')
        elif "id" in kwargs:
            pk = params.pop('id')

        if pk:
            ckey = get_cache_key_for_pk(self.model, pk, **params)
            obj = cache.get(ckey)
        
        if not obj:
            obj = super(CachedQuerySetMixIn, self).get(*args, **kwargs)
            cache.set(ckey, obj, self.cache_timeout)
            log.info("Orm cache missing: %s(%s)", 
                self.model.__name__, obj.id)
        else:
            log.info("Orm cache hit: %s(%s)", 
                self.model.__name__, obj.id)

        return obj

    def _clone(self, klass=None, **kwargs):
        """ Clone queryset. """
        qs = QuerySet._clone(self, klass, **kwargs)
        qs.cache_object_enable = self.cache_object_enable
        qs.cache_queryset_enable = self.cache_queryset_enable
        qs.cache_timeout = self.cache_timeout
        return qs

    def _prepare_queryset_for_cache(self, queryset):
        """
        This is where the magic happens. We need to first see if our result set
        is in the cache. If it isn't, we need to do the query and set the cache
        to (ModelClass, (*<pks>,), (*<select_related fields>,), <n keys>).
        """
        # TODO: make this split up large sets of data based on an option
        # and sets the last param, keys, to how many datasets are stored
        # in the cache to regenerate.

        keys = tuple(obj.pk for obj in queryset)
        fields = ()
        #if self._select_related:
        #    if not self._max_related_depth:
        #        fields = [f.name for f in opts.fields if f.rel and not f.null]
        #    else:
        #        # TODO: handle depth relate lookups
        #        fields = ()
        #else:
        #    fields = ()
        return (self.model, keys, fields, 1)

    def _get_queryset_from_cache(self, cache_object):
        """
        We transform the cache storage into an actual QuerySet object
        automagickly handling the keys depth and select_related fields (again,
        using the recursive methods of CachedQuerySetMixIn).
        
        We effectively would just be doing a cache.multi_get(*pks), grabbing
        the pks for each releation, e.g. user, and then doing a
        CachedManager.objects.filter() on them. This also then makes that
        queryset reusable. So the question is, should that queryset have been
        reusable? It could be invalidated by some other code which we aren't
        tieing directly into the parent queryset so maybe we can't do the
        objects.filter() query here and we have to do it internally.
        """
        # TODO: make this work for people who have, and who don't have, instance caching
        model, keys, fields, length = cache_object
        
        results = self._get_objects_for_keys(model, keys)
        if fields:
            # TODO: optimize this so it's only one get_many call instead of one per select_related field
            # XXX: this probably isn't handling depth beyond 1, didn't test even depth of 1 yet
            for f in fields:
                field = model._meta.get_field(f)
                field_results = dict((r.id, r) for r in  self._get_objects_for_keys(f.rel.to, [getattr(r, field.db_column) for r in results]))
                for r in results:
                    setattr(r, f.name, field_results[getattr(r, field.db_column)])
        return results

    def _get_objects_for_keys(self, model, keys):
        # First we fetch any keys that we can from the cache
        results = cache.get_many([get_cache_key_for_pk(model, k) for k in keys]).values()
        
        # Now we need to compute which keys weren't present in the cache
        result_ids = [obj.id for obj in results]
        missing = [key for key in keys if key not in result_ids]

        log.info("Orm cache queryset missing objects: %s(%s)",
            self.model.__name__, missing)
        # We no longer need to know what the keys were so turn it into a list
        results = list(results)
        objects = model._default_manager.filter(pk__in=missing)
        
        if objects:
            cache.set_many(dict([(obj.cache_key, obj) \
                for obj in objects]), self.cache_timeout)

        results.extend(objects)
        # Do a simple len() lookup (maybe we shouldn't rely on it returning the right
        # number of objects
        cnt = len(missing) - len(objects)
        if cnt:
            raise CacheMissingWarning("%d objects missing in the database" % (cnt,))
        return results        
    
    def _result_iter(self):
        if not self.cache_queryset_enable:
            return super(CachedQuerySetMixIn, self)._result_iter()

        from django.db.models.sql import query
        try:
            cached_qs = cache.get(self.query_key())
            if cached_qs: 
                results = self._get_queryset_from_cache(cached_qs)
                self._result_cache = results
                self.from_cache = True
                self._iter = None
                log.info("Orm cache queryset hit for %s", self.model.__name__)
            else:
                log.info("Orm cache queryset missing for %s", self.model.__name__)

        except query.EmptyResultSet:
            pass

        return super(CachedQuerySetMixIn, self)._result_iter()

    def _fill_cache(self, num=None):
        super(CachedQuerySetMixIn, self)._fill_cache(num=num)
        if not self._iter and not self.from_cache and self.cache_queryset_enable:
            qs_prepared_for_cache = self._prepare_queryset_for_cache(self._result_cache)
            cache.set(self.query_key(), qs_prepared_for_cache, self.cache_timeout)
            cache.set_many(dict([(obj.cache_key, obj) \
                for obj in self._result_cache]), self.cache_timeout)


class CachedQuerySet(CachedQuerySetMixIn, QuerySet):
    """
    Extends the QuerySet object and caches results via CACHE_BACKEND.
    """
    pass
