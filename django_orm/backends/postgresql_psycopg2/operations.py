# -*- coding: utf-8 -*-

from django import VERSION

if VERSION[:2] > (1,3):
    from django.db.backends.postgresql_psycopg2.operations \
        import DatabaseOperations as BaseDatabaseOperations
else:
    from django.db.backends.postgresql_psycopg2.base \
        import DatabaseOperations as BaseDatabaseOperations

class DatabaseOperations(BaseDatabaseOperations):
    def convert_values(self, value, field):
        """
        Coerce the value returned by the database backend into a consistent type that
        is compatible with the field type.
        """
        internal_type = field.get_internal_type()
        if internal_type in ('DecimalField', 'CharField', 'TextField'):
            return value
        elif internal_type and internal_type.endswith('IntegerField') or internal_type == 'AutoField':
            return int(value)
        elif internal_type in ('DateField', 'DateTimeField', 'TimeField'):
            return value
        # No field, or the field isn't known to be a decimal or integer
        # Default to a float
        return float(value)
