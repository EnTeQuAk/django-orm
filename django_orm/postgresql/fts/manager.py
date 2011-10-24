# -*- coding: utf-8 -*-

from django.utils.encoding import force_unicode
from django.db import models

class SearchManager(models.Manager):
    def __init__(self, fields=None, search_field='search_index', config='pg_catalog.english'):
        self.fields = None
        if fields is not None:
            if isinstance(fields, (list, tuple)):
                if len(fields) > 0:
                    if len(fields) > 0 and isinstance(fields[0], (list,tuple)):
                        self.fields = fields
                    else:
                        self.fields = [(x, None) for x in fields]

        self.vector_field = search_field
        self.default_weight = 'A'
        self.config = config
        super(SearchManager, self).__init__()

    def contribute_to_class(self, cls, name):
        setattr(cls, '_search_manager', self)
        super(SearchManager, self).contribute_to_class(cls, name)

    def _find_fields(self):
        fields = [f for f in self.model._meta.fields if isinstance(f,(models.CharField,models.TextField))]
        return [f.name for f in fields]

    def _vector_sql(self, field, weight=None, config=None):
        if not weight:
            weight = self.default_weight
        if not config:
            config = self.config
        f = self.model._meta.get_field(field)
        sql_template = "setweight(to_tsvector('%s', coalesce(unaccent(%s), '')), '%s')"
        return sql_template % (config, f.column, weight)

    def update_index(self, pk=None, config=None):
        sql_instances = []

        if not self.fields:
            self.fields = self._find_fields()

        for field, weight in self.fields:
            sql_instances.append(self._vector_sql(field, weight, config))

        vector_sql = ' || '.join(sql_instances)
        where_sql = ''
        
        if pk is not None:
            if isinstance(pk, (list, tuple)):
                where_sql = """ WHERE "%s" IN (%s)""" % \
                    (self.model._meta.pk.column, ','.join([str(v) for v in pk]))
            else:
                where_sql = """ WHERE "%s" IN (%s)""" % \
                    (self.model._meta.pk.column, pk)
        
        sql = """UPDATE "%s" SET "%s" = %s%s""" % \
            (self.model._meta.db_table, self.vector_field, vector_sql, where_sql)

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.execute("COMMIT;")
        cursor.close()

    def search(self, query, rank_field=None, rank_normalization=32, config=None):
        if not config:
            config = self.config
        
        ts_query = "to_tsquery('%s', unaccent('%s'))" % (config, force_unicode(query).replace("'","''"))
        where = """ "%s" @@ %s""" % (self.vector_field, ts_query)
        select_dict, order = {}, []

        if rank_field:
            select_dict[rank_field] = 'ts_rank("%s", %s, %d)' % \
                (self.vector_field, ts_query, rank_normalization)
            order = ['-%s' % (rank_field)]

        return self.all().extra(select=select_dict, where=[where], order_by=order)
