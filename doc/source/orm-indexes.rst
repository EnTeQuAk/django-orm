Own statements of indixes for a model
=====================================

It allows a simple way to add more additional indices to a particular model.

Supported backends: 

* ``django_orm.backends.postgresql_psycopg2``
* ``django_orm.backends.mysql``
* ``django_orm.backends.sqlite3``

How it works:
^^^^^^^^^^^^^

It is very simple, add the attribute ``indexes`` with a list of custom indices to ``_options`` dictionary
attribute on a model.

Example:

.. code-block:: python

    class Person(models.Model):
        name = models.CharField(max_length=200)

        _options = {
            'indexes':[
                'CREATE INDEX person_name_idx0 ON pages USING BTREE (lower(name));',
                'CREATE INDEX person_name_idx1 ON pages USING BTREE (lower(name) varchar_pattern_ops);',
            ]
        }


In postgresql, to use the unaccent lookup, we must have the extension installed! 
Furthermore, once installed,  you have to do a fix, which will create indexes 
with the function (postgresql 9.1 example):

.. code-block:: sql
    
    CREATE EXTENSION unaccent;
    ALTER FUNCTION unaccent(text) IMMUTABLE;

The other option is to install an alternative version unaccented:

.. code-block:: sql

    BEGIN;
    CREATE OR REPLACE FUNCTION unaccent(text) RETURNS text AS $$ 
    DECLARE input_string text := $1; 
    BEGIN 
        input_string := translate(input_string, 'àáâäãåāăąÀÁÂÄÃÅĀĂĄ', 'aaaaaaaaaaaaaaaaaa'); 
        input_string := translate(input_string, 'èéêëēĕėęěÈÉÊËÊĒĔĖĘĚ', 'eeeeeeeeeeeeeeeeeee'); 
        input_string := translate(input_string, 'ìíîïĩīĭÌÍÎÏĨĪĬ', 'iiiiiiiiiiiiii'); 
        input_string := translate(input_string, 'òóôöõōŏőÒÓÔÖÕŌŎŐ', 'oooooooooooooooo'); 
        input_string := translate(input_string, 'ùúûüũūŭůÙÚÛÜŨŪŬŮ', 'uuuuuuuuuuuuuuuu'); 
        input_string := translate(input_string, 'ñÑçÇ', 'nncc'); 
        return input_string; 
    END; $$ LANGUAGE plpgsql IMMUTABLE;
    COMMIT;
