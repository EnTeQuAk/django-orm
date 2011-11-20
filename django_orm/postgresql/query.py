# -*- coding: utf-8 -*-

from django import VERSION
from django.db.models.query import QuerySet
from django.db.models.sql.constants import SINGLE
from django.db.models.sql.datastructures import EmptyResultSet
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery
from django.db.models.sql.where import EmptyShortCircuit, WhereNode
from django.utils.encoding import force_unicode

try:
    from django.db.models.sql.where import QueryWrapper # django <= 1.3
except ImportError:
    from django.db.models.query_utils import QueryWrapper # django >= 1.4

from django_orm.postgresql.constants import QUERY_TERMS
from django_orm.postgresql.hstore.query import select_query, update_query
from django_orm.cache.query import CachedQuerySet


lookups = {
    'is_closed': lambda field, param: ('isclosed(%s) = %%s' % field, [param]),
    'is_open': lambda field, param: ('isclosed(%s) = %%s' % field, [param]),
    'area': lambda field, param: ('area(%s) = %%s' % field, [param]),
    'area_gt': lambda field, param: ('area(%s) > %%s' % field, [param]),
    'area_lt': lambda field, param: ('area(%s) < %%s' % field, [param]),
    'area_gte': lambda field, param: ('area(%s) >= %%s' % field, [param]),
    'area_lte': lambda field, param: ('area(%s) <= %%s' % field, [param]),
    'diameter': lambda field, param: ('diameter(%s) = %%s' % field, [param]),
    'diameter_gt': lambda field, param: ('diameter(%s) > %%s' % field, [param]),
    'diameter_lt': lambda field, param: ('diameter(%s) < %%s' % field, [param]),
    'diameter_gte': lambda field, param: ('diameter(%s) >= %%s' % field, [param]),
    'diameter_lte': lambda field, param: ('diameter(%s) <= %%s' % field, [param]),
    'length': lambda field, param: ('length(%s) = %%s' % field, [param]),
    'length_gt': lambda field, param: ('length(%s) > %%s' % field, [param]),
    'length_lt': lambda field, param: ('length(%s) < %%s' % field, [param]),
    'length_gte': lambda field, param: ('length(%s) >= %%s' % field, [param]),
    'length_lte': lambda field, param: ('length(%s) <= %%s' % field, [param]),
    'width': lambda field, param: ('width(%s) = %%s' % field, [param]),
    'width_gt': lambda field, param: ('width(%s) > %%s' % field, [param]),
    'width_lt': lambda field, param: ('width(%s) < %%s' % field, [param]),
    'width_gte': lambda field, param: ('width(%s) >= %%s' % field, [param]),
    'width_lte': lambda field, param: ('width(%s) <= %%s' % field, [param]),
    'npoints': lambda field, param: ('npoints(%s) = %%s' % field, [param]),
    'npoints_gt': lambda field, param: ('npoints(%s) > %%s' % field, [param]),
    'npoints_lt': lambda field, param: ('npoints(%s) < %%s' % field, [param]),
    'npoints_gte': lambda field, param: ('npoints(%s) >= %%s' % field, [param]),
    'npoints_lte': lambda field, param: ('npoints(%s) <= %%s' % field, [param]),
    'overlap': lambda field, param: ('%s && %%s' % field, [param]),
    'strictly_left_of': lambda field, param: ('%s << %%s' % field, [param]),
    'strictly_right_of': lambda field, param: ('%s >> %%s' % field, [param]),
    'strictly_below': lambda field, param: ('%s <<| %%s' % field, [param]),
    'strictly_above': lambda field, param: ('%s |>> %%s' % field, [param]),
    'notextendto_right_of': lambda field, param: ('%s &< %%s' % field, [param]),
    'notextendto_left_of': lambda field, param: ('%s &> %%s' % field, [param]),
    'notextend_above': lambda field, param: ('%s &<| %%s' % field, [param]),
    'notextend_below': lambda field, param: ('%s |&> %%s' % field, [param]),
    'intersects': lambda field, param: ('%s ?# %%s' % field, [param]),
    'is_horizontal': lambda field, param: ('(?- %s) = %%s' % field, [param]),
    'is_perpendicular': lambda field, param: ('%s ?-| %%s' % field, [param]),
    'is_parallel': lambda field, param: ('%s ?|| %%s' % field, [param]),
    'contained_in_or_on': lambda field, param: ('%s ?|| %%s' % field, [param]),
    'contains': lambda field, param: ('%s @> %%s' % field, [param]),
    'same_as': lambda field, param: ('%s ~= %%s' % field, [param]),
    'indexexact': lambda field, param: ('%s[%s] = %%s' % (field, param[0]+1), [param[1]]),
    'distinct': lambda field, param: ('%s <> %%s' % field, [param]),
    'contains': lambda field, param, is_list: ('%s @> %%s' % field, [param]) \
        if is_list else ('%%s = ANY(%s)' % field, [param]),
    'containedby': lambda field, param: ('%s <@ %%s' % field, [param]),
    'unaccent': lambda field, param: ('unaccent(%s) LIKE unaccent(%%s)' % field, [param]),
    'iunaccent': lambda field, param: ('lower(unaccent(%s)) LIKE lower(unaccent(%%s))' %\
        field, [param]),
}

geometric_types = ('box', 'point', 'line', 'lseg', 'path', 'polygon', 'circle')

class PgWhereNode(WhereNode):
    def make_atom(self, child, qn, connection):
        lvalue, lookup_type, value_annot, params_or_value = child
        kwargs = {'connection': connection} if VERSION[:2] >= (1, 3) else {}

        if hasattr(lvalue, 'process'):
            try:
                lvalue, params = lvalue.process(lookup_type, params_or_value, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet
        else:
            params = Field().get_db_prep_lookup(lookup_type, params_or_value,
                prepared=True, **kwargs)

        model_alias, field_name, db_type = lvalue
        field_sql = self.sql_for_columns(lvalue, qn, connection)
        
        if db_type in geometric_types and lookup_type in lookups:
            return lookups[lookup_type](field_sql, params)

        elif '[]' in db_type:
            params, is_list = params
            if lookup_type == 'contains':   
                a = lookups[lookup_type](field_sql, params, is_list)
                return a
            elif lookup_type in lookups:
                return lookups[lookup_type](field_sql, params)
            else:
                return super(PgWhereNode, self).make_atom(child, qn, connection)

        elif 'varchar' in db_type:
            if lookup_type in ('unaccent', 'iunaccent'):
                return lookups[lookup_type](field_sql, params)
            else:
                return super(PgWhereNode, self).make_atom(child, qn, connection)

        elif db_type == 'tsvector':
            if isinstance(params, basestring):
                query, config = params, 'pg_catalog.english'
            elif isinstance(params, (list, tuple)):
                query, config = params
            else:
                raise TypeError('invalid params')
            
            if lookup_type == 'query':
                return ("%s @@ to_tsquery('%s', unaccent('%s'))" % \
                    (field_sql, config, force_unicode(query).replace("'","''")), [])
            else:
                raise TypeError('invalid lookup type')

        return super(PgWhereNode, self).make_atom(child, qn, connection)


class PgQuery(Query):
    query_terms = QUERY_TERMS
    def __init__(self, model):
        super(PgQuery, self).__init__(model, where=PgWhereNode)


class PgQuerySet(CachedQuerySet):
    def __init__(self, model=None, query=None, using=None):
        query = query or PgQuery(model)
        super(PgQuerySet, self).__init__(model=model, query=query, using=using)

    @select_query
    def array_slice(self, query, attr, x, y):
        query.add_extra({'_': '%s[%%s:%%s]' % attr}, [x+1, y+1], None, None, None, None)
        result = query.get_compiler(self.db).execute_sql(SINGLE)
        if result and result[0]:
            field = self.model._meta.get_field_by_name(attr)[0]
            return field.to_python(result[0])
        return result[0]

    @select_query
    def array_length(self, query, attr):
        query.add_extra({'_': 'array_length(%s, 1)' % attr}, [], None, None, None, None)
        result = query.get_compiler(self.db).execute_sql(SINGLE)
        if result and result[0]:
            field = self.model._meta.get_field_by_name(attr)[0]
            return field.to_python(result[0])
        return result[0]

