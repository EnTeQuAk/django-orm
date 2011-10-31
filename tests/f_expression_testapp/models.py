# -*- coding: utf-8 -*-

from django.db import models

class TestModel(models.Model):
    done = models.BooleanField(default=False)
    done2 = models.BooleanField(default=False)
