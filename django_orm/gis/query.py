# -*- coding: utf-8 -*-

from django.contrib.gis.db.models.query import GeoQuerySet as BaseGeoQuerySet
from django_orm.cache.query import CachedMixIn

""" TODO:
improve and delete repeated code.
"""

class GeoQuerySet(CachedMixIn, BaseGeoQuerySet):
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
