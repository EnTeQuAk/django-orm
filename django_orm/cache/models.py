from django.db.models.manager import Manager
from django.db.models.base import ModelBase, Model
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.fields import FieldDoesNotExist
from django.db.models.options import Options
from django.db.models import signals
from django.db.models.loading import register_models, get_model
from django.dispatch import dispatcher
from django.utils.functional import curry
from django.conf import settings

from django.core.cache import cache

import types
import sys

from django_orm.manager import Manager as CacheManager
from django_orm.cache.utils import get_cache_key_for_pk

class CachingMixin(object):
    cached_objects = CacheManager()

    @staticmethod
    def _get_cache_key_for_pk(model, pk):
        return get_cache_key_for_pk(model, pk)
    
    @property
    def cache_key(self):
        return self._get_cache_key_for_pk(self.__class__, self.pk)
