# -*- coding: utf-8 -*-

from django import VERSION
from django.db.models.query import QuerySet
from django.db.models.sql.constants import SINGLE
from django.db.models.sql.datastructures import EmptyResultSet
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery
from django.db.models.sql.where import EmptyShortCircuit, WhereNode

try:
    from django.db.models.sql.where import QueryWrapper # django <= 1.3
except ImportError:
    from django.db.models.query_utils import QueryWrapper # django >= 1.4

from django_orm.mysql.constants import QUERY_TERMS

class MyWhereNode(WhereNode):
    def make_atom(self, child, qn, connection):
        lvalue, lookup_type, value_annot, param = child
        kwargs = {'connection': connection} if VERSION[:2] >= (1, 3) else {}

        if not lvalue.field:
            return super(MyWhereNode, self).make_atom(child, qn, connection)

        if not hasattr(lvalue.field, 'db_type'):
            return super(MyWhereNode, self).make_atom(child, qn, connection)

        db_type = lvalue.field.db_type(**kwargs)
        if lvalue and lvalue.field and hasattr(lvalue.field, 'db_type') \
                and "varchar" in db_type:

            try:
                lvalue, params = lvalue.process(lookup_type, param, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet
            
            field = self.sql_for_columns(lvalue, qn, connection)
            if lookup_type in ['unaccent', 'iunaccent']:
                return ("%s LIKE _utf8 %%s COLLATE utf8_unicode_ci" % field, ["%" + param + "%"])
            else:
                return super(MyWhereNode, self).make_atom(child, qn, connection)

        return super(MyWhereNode, self).make_atom(child, qn, connection)


class MyQuery(Query):
    query_terms = QUERY_TERMS
    def __init__(self, model):
        super(MyQuery, self).__init__(model, where=MyWhereNode)


from django_orm.cache.query import CachedQuerySet

class MyQuerySet(CachedQuerySet):
    def __init__(self, model=None, query=None, using=None):
        query = query or MyQuery(model)
        super(MyQuerySet, self).__init__(model=model, query=query, using=using)
