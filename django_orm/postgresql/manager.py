# -*- coding: utf-8 -*-

from django.db import models
from django_orm.postgresql.query import PgQuerySet

class PgManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return PgQuerySet(self.model, using=self._db)

    def array_slice(self, attr, x, y, **params):
        """ Get subarray from some array field. """
        return self.filter(**params).array_slice(attr, x, y)

    def array_length(self, attr, **params):
        """Get length from some array field"""
        return self.filter(**params).array_length(attr)
