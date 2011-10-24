# -*- coding: utf-8 -*-

from django.db import models

class UnaccentAggregate(models.sql.aggregates.Aggregate):
    sql_function = 'unaccent'
    sql_template = '%(function)s(%(field)s)'

    def __init__(self, col, source=None, is_summary=False, **extra):
        self.col = col
        self.source = source
        self.is_summary = is_summary
        self.extra = extra
        self.field = models.sql.aggregates.AggregateField('CharField')
        

class Unaccent(models.Aggregate):
    name = 'UnaccentAggregate'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = UnaccentAggregate(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate


class ArrayLengthAggregate(models.sql.aggregates.Aggregate):
    sql_function = 'array_length'
    sql_template = '%(function)s(%(field)s, 1)'
    is_computed = True

    def __init__(self, col, source=None, is_summary=True, **extra):
        self.col, self.source, self.is_summary = col, source, is_summary
        self.extra = extra
        self.field = models.sql.aggregates.AggregateField('ArrayField')

        if 'sum' in extra and extra['sum']:
            self.sql_template = "sum(%s)" % (self.sql_template)


class ArrayLength(models.Aggregate):
    """
    Aggregate: returns the length of the requested array.
    """

    name = "ArrayLengthAggregate"

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = ArrayLengthAggregate(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate
