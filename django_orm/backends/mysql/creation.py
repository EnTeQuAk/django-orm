# -*- coding: utf-8 -*-

from django.db.backends.mysql.creation import DatabaseCreation as BaseDatabaseCreation

class DatabaseCreation(BaseDatabaseCreation):
    def sql_indexes_for_model(self, model, style):
        output = super(DatabaseCreation, self).sql_indexes_for_model(model, style)
        
        meta = getattr(model, '_orm_meta', None)
        if not meta:
            return output
        
        indexes = getattr(meta, 'indexes', [])
        if not isinstance(indexes, (list, tuple)):
            raise Exception("aditional_indexes must be a list or tuple")
        
        for indexitem in indexes:
            if indexitem.endswith(";"):
                output.append(indexitem)
        return output
