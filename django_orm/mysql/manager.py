# -*- coding: utf-8 -*-

from django.db import models
from django_orm.mysql.query import MyQuerySet

class MyManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return MyQuerySet(self.model, using=self._db)
