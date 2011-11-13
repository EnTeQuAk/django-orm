# -*- coding: utf-8 -*-

from django.utils.encoding import force_unicode
from django.db import models, connections, connection
from django.db.models import signals

from django_orm.postgresql.fts.mixin import SearchManagerMixIn
from django_orm.cache.invalidator import invalidate_object

import logging; log = logging.getLogger('orm.cache')

class ManagerMixIn(object):
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
            return super(ManagerMixIn, self).get_query_set()

    def cache(self, *args, **kwargs):
        """ Active cache for this queryset """
        return self.get_query_set().cache(*args, **kwargs)

    def no_cache(self, *args, **kwargs):
        """ Deactive cache for this queryset. """
        return self.get_query_set().no_cache(*args, **kwargs)

    def array_slice(self, attr, x, y, **params):
        """ Get subarray from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_slice(attr, x, y)

    def array_length(self, attr, **params):
        """Get length from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_length(attr)

    def contribute_to_class(self, model, name):
        if not getattr(model, '_orm_manager', None):
            model._orm_manager = self

        signals.post_save.connect(invalidate_object, sender=model)
        signals.post_delete.connect(invalidate_object, sender=model)
        super(ManagerMixIn, self).contribute_to_class(model, name)

    def clear_cache(self):
        """Dummy method."""
        pass


class Manager(ManagerMixIn, models.Manager):
    use_for_related_fields = True


class FTSManager(SearchManagerMixIn, ManagerMixIn, models.Manager):
    """ Manager with postgresql full text search mixin. """
    use_for_related_fields = True


from .dispatch import *
