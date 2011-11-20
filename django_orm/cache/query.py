# -*- coding: utf-8 -*-

from django.db.models.query import QuerySet, ValuesQuerySet, ValuesListQuerySet
from django.db.models.query import ITER_CHUNK_SIZE
from django.db import backend, connection
from django.conf import settings

from django_orm.cache.utils import get_cache_key_for_pk, get_cache
from django_orm.cache.exceptions import CacheMissingWarning
from django_orm.postgresql import server_side_cursors

CACHE_KEY_PREFIX = getattr(settings, 'ORM_CACHE_KEY_PREFIX', 'orm.cache')
CACHE_FETCH_BY_ID = getattr(settings, 'ORM_CACHE_FETCH_BY_ID', False)

import copy, hashlib
import logging; log = logging.getLogger('orm.cache')

cache = get_cache()


class CachedMixIn(object):
    from_cache = False
    cache_object_enable = False
    cache_queryset_enable = False
    cache_fetch_by_id = False
    cache_fetch_by_id_queryset = False

    def __init__(self, *args, **kwargs):
        self.cache_key_prefix = CACHE_KEY_PREFIX
        super(CachedMixIn, self).__init__(*args, **kwargs)

        orm_meta = getattr(self.model, '_orm_meta')
        options = getattr(orm_meta, 'options')

        self.cache_object_enable = options['cache_object']
        self.cache_queryset_enable = options['cache_queryset']
        self.cache_timeout = options['default_timeout']

    def query_key(self):
        sql, params = self.query.get_compiler(using=self.db).as_sql()
        return "%s:qs:default:table:%s:%s" % (
            CACHE_KEY_PREFIX,
            self.model._meta.db_table,
            hashlib.sha1(sql % params).hexdigest()
        )

    def _clone(self, klass=None, **kwargs):
        """ Clone queryset. """
        qs = super(CachedMixIn,self)._clone(klass, **kwargs)
        qs.cache_object_enable = self.cache_object_enable
        qs.cache_queryset_enable = self.cache_queryset_enable
        qs.cache_timeout = self.cache_timeout
        qs.cache_fetch_by_id = self.cache_fetch_by_id
        qs.cache_fetch_by_id_queryset = self.cache_fetch_by_id_queryset
        return qs

    def cache(self, timeout=None):
        if not timeout:
            timeout = self.cache_timeout

        qs = self._clone()
        qs.cache_object_enable = True
        qs.cache_queryset_enable = True
        qs.cache_timeout = timeout
        return qs

    def no_cache(self):
        qs = self._clone()
        qs.cache_object_enable = False
        qs.cache_queryset_enable = False
        qs.cache_timeout = self.cache_timeout
        return qs

    def byid(self, cache_qs=False):
        qs = self._clone()
        qs.cache_fetch_by_id = True
        qs.cache_fetch_by_id_queryset = cache_qs
        return qs

    def get(self, *args, **kwargs):
        if not self.cache_object_enable:
            return super(CachedMixIn, self).get(*args, **kwargs)

        if len(args) > 0:
            return super(CachedMixIn, self).get(*args, **kwargs)
        
        pk, params, obj = None, copy.deepcopy(kwargs), None
        if "pk" in params:
            pk = params.pop('pk')
        elif "id" in kwargs:
            pk = params.pop('id')

        if pk:
            ckey = get_cache_key_for_pk(self.model, pk, **params)
            obj = cache.get(ckey)
        
            if not obj:
                obj = super(CachedMixIn, self).get(*args, **kwargs)
                cache.set(ckey, obj, self.cache_timeout)
                log.info("Orm cache missing: %s(%s)", 
                    self.model.__name__, obj.id)
            else:
                log.info("Orm cache hit: %s(%s)", 
                    self.model.__name__, obj.id)
        else:
            obj = super(CachedMixIn, self).get(*args, **kwargs)
        return obj

    def _prepare_queryset_for_cache(self, queryset):
        keys = tuple(obj.pk for obj in queryset)
        fields = ()
        return (self.model, keys, fields, 1)

    def _get_queryset_from_cache(self, cache_object):
        model, keys, fields, length = cache_object
        results = self._get_objects_for_keys(model, keys)

        #if fields:
        #    # TODO: optimize this so it's only one get_many call instead of one per select_related field
        #    # XXX: this probably isn't handling depth beyond 1, didn't test even depth of 1 yet
        #    for f in fields:
        #        field = model._meta.get_field(f)
        #        field_results = dict((r.id, r) for r in  self._get_objects_for_keys(f.rel.to, [getattr(r, field.db_column) for r in results]))
        #        for r in results:
        #            setattr(r, f.name, field_results[getattr(r, field.db_column)])
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
        objects = model._orm_manager.no_cache().filter(pk__in=missing)
        
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
            return super(CachedMixIn, self)._result_iter()
        
        if self.cache_fetch_by_id and not self.cache_fetch_by_id_queryset:
            return super(CachedMixIn, self)._result_iter()
        
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
        return super(CachedMixIn, self)._result_iter()

    
class CachedQuerySet(CachedMixIn, QuerySet):
    """ Main subclass of QuerySet that implements cache subsystem. """
    def _fill_cache(self, num=None):
        super(CachedQuerySet, self)._fill_cache(num=num)
        if not self._iter and not self.from_cache and self.cache_queryset_enable:
            qs_prepared_for_cache = self._prepare_queryset_for_cache(self._result_cache)
            cache.set(self.query_key(), qs_prepared_for_cache, self.cache_timeout)
            cache.set_many(dict([(obj.cache_key, obj) \
                for obj in self._result_cache]), self.cache_timeout)

    def values(self, *fields):
        return self._clone(klass=CachedValuesQuerySet, setup=True, _fields=fields)

    def values_list(self, *fields, **kwargs):
        flat = kwargs.pop('flat', False)
        if kwargs:
            raise TypeError('Unexpected keyword arguments to values_list: %s'
                % (kwargs.keys(),))
        if flat and len(fields) > 1:
            raise TypeError("'flat' is not valid when values_list is called with more than one field.")
        return self._clone(klass=CachedValuesListQuerySet, setup=True, flat=flat,
            _fields=fields)

    def iterator(self):
        if self.cache_fetch_by_id:
            return self.fetch_by_id()

        return super(CachedMixIn, self).iterator()

    def fetch_by_id(self):
        if self.cache_fetch_by_id_queryset and self.cache_queryset_enable:
            vals = self.values_list('pk', *self.query.extra.keys())
        else:
            vals = self.no_cache().values_list('pk', *self.query.extra.keys())
        
        ids = [val[0] for val in vals]
        if self.cache_object_enable:
            keys = dict((get_cache_key_for_pk(self.model, i), i) for i in ids)
            cached = dict((k, v) for k, v in cache.get_many(keys).items() if v is not None)
            missed = [pk for key, pk in keys.iteritems() if key not in cached]
            new = {}

            if missed:
                objects = self.model._default_manager.filter(pk__in=missed)
                new = dict((get_cache_key_for_pk(self.model, o.pk), o) \
                                                        for o in objects)
                cache.set_many(new)

            objects = dict((o.pk, o) for o in cached.values() + new.values())
            for pk in ids:
                yield objects[pk]

        else:
            qs = self.model._orm_manager.no_cache().filter(pk__in=ids)
            if connection.vendor == 'postgresql':
                with server_side_cursors(qs, itersize=10):
                    for obj in qs.iterator():
                        yield obj
            else:
                for obj in qs.iterator():
                    yield obj
 

class CachedValuesMixIn(object):
    cache_modifier = 'values'

    def _prepare_queryset_for_cache(self, queryset):
        return (self.model, queryset, (), 1)

    def _get_queryset_from_cache(self, cache_object):
        model, keys, fields, length = cache_object
        return keys

    def _fill_cache(self, num=None):
        super(CachedValuesMixIn, self)._fill_cache(num=num)
        if not self._iter and not self.from_cache and self.cache_queryset_enable:
            qs_prepared_for_cache = self._prepare_queryset_for_cache(self._result_cache)
            cache.set(self.query_key(), qs_prepared_for_cache, self.cache_timeout)

    def query_key(self):
        sql, params = self.query.get_compiler(using=self.db).as_sql()
        return "%s:qs:%s:table:%s:%s:flat=%s" % (
            CACHE_KEY_PREFIX,
            self.cache_modifier,
            self.model._meta.db_table,
            hashlib.sha1(sql % params).hexdigest(),
            getattr(self,'flat', False),
        )


class CachedValuesQuerySet(CachedValuesMixIn, CachedMixIn, ValuesQuerySet):
    cache_modifier = 'values'


class CachedValuesListQuerySet(CachedValuesMixIn, CachedMixIn, ValuesListQuerySet):
    cache_modifier = 'valueslist'
