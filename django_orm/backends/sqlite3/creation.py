# -*- coding: utf-8 -*-

from django.db.backends.sqlite3.creation import DatabaseCreation as BaseDatabaseCreation

class DatabaseCreation(BaseDatabaseCreation):
    def sql_indexes_for_model(self, model, style):
        output = super(DatabaseCreation, self).sql_indexes_for_model(model, style)
        additional_indexes = getattr(model, 'additional_indexes', [])
        if not isinstance(additional_indexes, (list, tuple)):
            raise Exception("aditional_indexes must be a list or tuple")
        
        for indexitem in additional_indexes:
            if indexitem.endswith(";"):
                output.append(indexitem)
        return output
