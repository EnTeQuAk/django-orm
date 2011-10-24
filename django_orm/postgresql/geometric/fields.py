# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_unicode
from django_orm.postgresql.constants import geometric_lookups

"""
Posible aggregate list:
- area(object)          -> double
- center(object)        -> point
- diameter(circle)      -> double
- height(box)           -> double
- isclosed(path)        -> bool
- isopen(path)          -> bool
- length(object)        -> double
- npoints(path, polygon)-> int
- radius(circle)        -> double
- width(box)            -> double

A lot of agregates are used for querys.

"""

class PointField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(PointField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('same_as', 'distance'):
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'point'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class CircleField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(CircleField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'circle'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class LineField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(LineField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        #fix this with correct lookup types not all
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'line'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class LsegField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(LsegField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        #fix this with correct lookup types not all
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'lseg'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class BoxField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(BoxField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        #fix this with correct lookup types not all
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'box'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class PathField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(PathField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        #fix this with correct lookup types not all
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'path'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value


class PolygonField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(PolygonField, self).__init__(*args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        #fix this with correct lookup types not all
        if lookup_type in geometric_lookups:
            return self.get_prep_value(value)
        raise TypeError("Field has invalid lookup: %s" % lookup_type)

    def db_type(self, connection):
        return 'box'

    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        return value

    def to_python(self, value):
        return value
