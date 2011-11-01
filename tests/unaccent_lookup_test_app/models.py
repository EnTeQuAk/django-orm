# -*- coding: utf-8 -*-

from django.db import models
from django_orm.manager import Manager
from django_orm.fields.standard import CharField

class TestModel(models.Model):
    name = CharField(max_length=200)
    objects = Manager()
