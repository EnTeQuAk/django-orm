# -*- coding: utf-8 -*-
from django.db.models import signals
from django_orm.manager import Manager

def ensure_default_manager(sender, **kwargs):
    cls = sender
    cls.add_to_class('objects', Manager()) 

signals.class_prepared.connect(ensure_default_manager)
