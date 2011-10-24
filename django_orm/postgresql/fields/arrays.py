# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_unicode

class ArrayField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self._array_type = kwargs.pop('dbtype', 'int')
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(ArrayField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """

        if hasattr(value, 'prepare'):
            return value.prepare()
        if hasattr(value, '_prepare'):
            return value._prepare()

        if lookup_type in ('indexexact', 'distinct', 'slice',\
                    'contains', 'containedby', 'overlap', 'exact', \
                    'gt','lt','gte', 'lte'):
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return '%s[]' % self._array_type

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        if not value:
            return value

        if self._array_type in ('text') or "varchar" in self._array_type:
            value = map(force_unicode, value)

        return value

    def get_prep_value(self, value):
        return value

    def to_python(self, value):
        if value and isinstance(value, (list,tuple)):
            if self._array_type in ('text') or "varchar" in self._array_type:
                return map(lambda x: x.decode('utf-8'), value)
        return value
