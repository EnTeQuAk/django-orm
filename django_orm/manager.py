# -*- coding: utf-8 -*-

from django.db import models, connections
from django.core.cache import cache
from django.conf import settings
from django.db.models import signals

DEFAULT_CACHE_TIMEOUT = getattr(settings, 'ORM_CACHE_DEFAULT_TIMEOUT', 30)
DEFAULT_CACHE_ENABLED = getattr(settings, 'ORM_CACHE_DEFAULT_ENABLED', False)

class Manager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        connection = connections[self.db]
        if connection.vendor == 'postgresql':
            from django_orm.postgresql.query import PgQuerySet
            return PgQuerySet(model=self.model, using=self._db)
        elif connection.vendor == 'mysql':
            from django_orm.mysql.query import MyQuerySet
            return MyQuerySet(model=self.model, using=self._db)
        elif connection.vendor == 'sqlite':
            from django_orm.sqlite3.query import SqliteQuerySet
            return SqliteQuerySet(model=self.model, using=self._db)
        else:
            return super(Manager, self).get_query_set()

    def cache(self, *args, **kwargs):
        return self.get_query_set().cache(*args, **kwargs)

    def array_slice(self, attr, x, y, **params):
        """ Get subarray from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_slice(attr, x, y)

    def array_length(self, attr, **params):
        """Get length from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_length(attr)

    def contribute_to_class(self, model, name):
        super(Manager, self).contribute_to_class(model, name)
        options = getattr(model, 'additional_options', None)
        options_are_none  = False
        
        if options is None:
            options = {}
            options_are_none = True
        
        if 'cache_object' not in options:
            options['cache_object'] = DEFAULT_CACHE_ENABLED

        if 'cache_queryset' not in options:
            options['cache_queryset'] = DEFAULT_CACHE_ENABLED
        elif options['cache_queryset']:
            options['cache_object'] = True
    
        if options['cache_object']:
            signals.post_save.connect(self.invalidate_object, sender=model)
            signals.post_delete.connect(self.invalidate_object, sender=model)

        if options_are_none:
            model.additional_options = options

        print model.additional_options

    def invalidate_object(self, instance, **kwargs):
        cache.delete(instance.cache_key)

