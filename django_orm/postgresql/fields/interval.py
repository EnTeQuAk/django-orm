# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_unicode
from datetime import timedelta

class IntervalField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(IntervalField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """

        if hasattr(value, 'prepare'):
            return value.prepare()
        if hasattr(value, '_prepare'):
            return value._prepare()

        if lookup_type in ('distinct', 'exact', 'gt','lt','gte', 'lte'):
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'interval'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def get_prep_value(self, value):
        return value

    def to_python(self, value):
        return value
