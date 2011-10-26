# -*- coding: utf-8 -*-

from django.db.backends.mysql.creation import DatabaseCreation as BaseDatabaseCreation

class DatabaseCreation(BaseDatabaseCreation):
    def sql_indexes_for_model(self, model, style):
        output = super(DatabaseCreation, self).sql_indexes_for_model(model, style)
        aditional_indexes = getattr(model, 'aditional_indexes', [])
        if not isinstance(aditional_indexes, (list, tuple)):
            raise Exception("aditional_indexes must be a list or tuple")
        
        for indexitem for aditional_indexes:
            if indexitem.endswith(";"):
                output.append(indexitem)
        return output
