# -*- coding: utf-8 -*-

from django.db import models

class VectorField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['default'] = ''
        kwargs['editable'] = False
        kwargs['serialize'] = False
        kwargs['db_index'] = True
        super(VectorField, self).__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        return 'tsvector'

    def get_prep_lookup(self, lookup_type, value):
        if hasattr(value, 'prepare'):
            return value.prepare()

        if hasattr(value, '_prepare'):
            return value._prepare()

        if lookup_type == 'query':
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def get_prep_value(self, value):
        return value
