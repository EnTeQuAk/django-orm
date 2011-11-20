# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields import CharField as BaseCharField

class CharField(BaseCharField):
    __metaclass__ = models.SubfieldBase

    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """

        if lookup_type in ('unaccent', 'iunaccent'):
            return self.get_prep_value(value)
        return super(CharField, self).get_prep_lookup(lookup_type, value)

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        value = self.get_prep_lookup(lookup_type, value)
        return "%%%s%%" % value
