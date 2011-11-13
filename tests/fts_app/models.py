# -*- coding: utf-8 -*-

from django.db import models
from django_orm.postgresql.fts.fields import VectorField
from django_orm.manager import FTSManager

class Person(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    search_index = VectorField()

    objects = FTSManager(
        fields=('name', 'description'),
        search_field = 'search_index',
    )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        if hasattr(self, '_orm_manager'):
            self._orm_manager.update_index(pk=self.pk)
