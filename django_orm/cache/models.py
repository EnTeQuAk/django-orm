# -*- coding: utf-8 -*-

from django.conf import settings
from django_orm.manager import Manager as CacheManager
from django_orm.cache.utils import get_cache_key_for_pk

class CachingMixin(object):
    @staticmethod
    def _get_cache_key_for_pk(model, pk):
        return get_cache_key_for_pk(model, pk)
    
    @property
    def cache_key(self):
        return self._get_cache_key_for_pk(self.__class__, self.pk)
