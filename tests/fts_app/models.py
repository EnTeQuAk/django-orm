# -*- coding: utf-8 -*-

from django.db import models
from django_orm.postgresql.fts.fields import VectorField
from django_orm.postgresql.fts.manager import SearchManager

class Person(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    search_index = VectorField()

    objects = SearchManager(
        fields=('name', 'description'),
        search_field = 'search_index',
    )

    _options = {
        "manager": False,
    }

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        if hasattr(self, '_search_manager'):
            self._search_manager.update_index(pk=self.pk)
