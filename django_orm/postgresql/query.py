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


class PgWhereNode(WhereNode):
    def make_atom(self, child, qn, connection):
        lvalue, lookup_type, value_annot, param = child
        kwargs = {'connection': connection} if VERSION[:2] >= (1, 3) else {}

        if not lvalue.field:
            return super(PgWhereNode, self).make_atom(child, qn, connection)

        if not hasattr(lvalue.field, 'db_type'):
            return super(PgWhereNode, self).make_atom(child, qn, connection)

        db_type = lvalue.field.db_type(**kwargs)
        if lvalue and lvalue.field and hasattr(lvalue.field, 'db_type') \
            and db_type in ('box', 'point', 'line', 'lseg', 'path', 'polygon', 'circle'):
            
            # TODO: use dict for fat lookup of lookups (?) (this makes this method
            # more readable and more fast... make benchmarks...
            
            try:
                lvalue, params = lvalue.process(lookup_type, param, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet

            field = self.sql_for_columns(lvalue, qn, connection)
            if lookup_type == 'is_closed':
                return ('isclosed(%s) = %%s' % field, [param])

            elif lookup_type == 'is_open':
                return ('isopen(%s) = %%s' % field, [param])

            elif lookup_type.split("_", 1)[0] in \
                    ('area','diameter','radius','length', 'width', 'npoints'):

                lookup = lookup_type.split("_", 1)
                if len(lookup) < 2:
                    return ('%s(%s) = %%s' % (lookup[0], field), [param])
                elif lookup[1] == 'gt':
                    return ('%s(%s) > %%s' % (lookup[0], field), [param])
                elif lookup[1] == 'lt':
                    return ('%s(%s) < %%s' % (lookup[0], field), [param])
                elif lookup[1] == 'gte':
                    return ('%s(%s) >= %%s' % (lookup[0], field), [param])
                elif lookup[1] == 'lte':
                    return ('%s(%s) <= %%s' % (lookup[0], field), [param])
                else:
                    raise TypeError('invalid lookup type')

            elif lookup_type == 'overlap':
                return ('%s && %%s' % field, [param])

            elif lookup_type.startswith('strictly_'):
                if lookup_type == 'strictly_left_of':
                    return ('%s << %%s' % field, [param])
                elif lookup_type == 'strictly_right_of':
                    return ('%s >> %%s' % field, [param])
                elif lookup_type == 'strictly_below':
                    return ('%s <<| %%s' % field, [param])
                elif lookup_type == 'strictly_above':
                    return ('%s |>> %%s' % field, [param])
                else:
                    raise TypeError('invalid lookup type')
            elif lookup_type == 'notextendto_right_of':
                return ('%s &< %%s' % field, [param])
            elif lookup_type == 'notextendto_left_of':
                return ('%s &> %%s' % field, [param])
            elif lookup_type == 'notextend_above':
                return ('%s &<| %%s' % field, [param])
            elif lookup_type == 'notextend_below':
                return ('%s |&> %%s' % field, [param])
            elif lookup_type == 'intersects':
                return ('%s ?# %%s' % field, [param])
            elif lookup_type == 'is_horizontal':
                return ('(?- %s) = %%s' % field, [param])
            elif lookup_type == 'is_perpendicular':
                return ('%s ?-| %%s' % field, [param])
            elif lookup_type == 'is_parallel':
                return ('%s ?|| %%s' % field, [param])
            elif lookup_type == 'contained_in_or_on':
                return ('%s <@ %%s' % field, [param])
            elif lookup_type == 'contains':
                return ('%s @> %%s' % field, [param])
            elif lookup_type == 'same_as':
                return ('%s ~= %%s' % field, [param])
            else:
                raise TypeError('invalid lookup type')

        elif lvalue and lvalue.field and hasattr(lvalue.field, 'db_type') \
                and '[]' in db_type:

            try:
                lvalue, params = lvalue.process(lookup_type, param, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet
            
            field = self.sql_for_columns(lvalue, qn, connection)

            is_list = True

            # first test nonstandard lookups
            if lookup_type == 'indexexact':
                if len(param) == 2 and isinstance(param[0], int) \
                    and isinstance(param[1], (int, str, unicode)):
                    return ('%s[%s] = %%s' % (field, param[0]+1), [param[1]])
                else:
                    raise ValueError('invalid value')

            if isinstance(param, (list, tuple)):
                if isinstance(param[0], (str, unicode)):
                    param = u"{%s}" % (",".join(['"%s"' % x for x in param]))
                elif isinstance(param[0], (float, int, long)):
                    param = u"{%s}" % (",".join(map(str, param)))
                else:
                    raise ValueError('invalid value')
            else:
                is_list = False

            if lookup_type == 'distinct':
                return ('%s <> %%s' % field, [param])

            elif lookup_type == 'contains':
                if is_list: return ('%s @> %%s' % field, [param])
                else: return ('%%s = ANY(%s)' % field, [param])

            elif lookup_type == 'containedby':
                return ('%s <@ %%s' % field, [param])

            elif lookup_type == 'overlap':
                # Have elements in common
                return ('%s && %%s' % field, [param])
            
            elif lookup_type in ('gt', 'gte', 'lt', 'lte', 'isnull', 'exact'):
                return super(PgWhereNode, self).make_atom(child, qn, connection)

            else:
                raise TypeError('invalid lookup type')


        elif lvalue and lvalue.field and hasattr(lvalue.field, 'db_type') \
                and "varchar" in db_type:
            try:
                lvalue, params = lvalue.process(lookup_type, param, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet
            
            field = self.sql_for_columns(lvalue, qn, connection)

            if lookup_type == 'unaccent':
                return ('unaccent(%s) LIKE unaccent(%%s)' % field, ["%" + param + "%"])
            elif lookup_type == 'iunaccent':
                return ('lower(unaccent(%s)) LIKE lower(unaccent(%%s))' % field, ["%" + param + "%"])
            else:
                return super(PgWhereNode, self).make_atom(child, qn, connection)

        elif lvalue and lvalue.field and hasattr(lvalue.field, 'db_type') \
            and db_type == 'tsvector':

            try:
                lvalue, params = lvalue.process(lookup_type, param, connection)
            except EmptyShortCircuit:
                raise EmptyResultSet
            
            field = self.sql_for_columns(lvalue, qn, connection)

            if isinstance(param, (list, tuple)):
                query, config = param
            else:
                query, config = param, 'pg_catalog.english'

            if lookup_type == 'query':
                return ("%s @@ to_tsquery('%s', unaccent('%s'))" % \
                    (field, config, force_unicode(query).replace("'","''")), [])
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

