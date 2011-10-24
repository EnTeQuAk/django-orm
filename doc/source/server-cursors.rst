PostgreSQL Server-Side cursors
==============================

For most cases, the normal cursor and django psycopg2 are more than enough. 
But there are cases where we have to do queries to tables with large amounts of 
data, and we need an efficient way to query this data.


Example usage:
^^^^^^^^^^^^^^

.. code-block:: python

    from django_postgresql import server_side_cursors

    qs = Model.objects.all()
    with server_side_cursors(qs, itersize=100):
        for item in qs.iterator():
            print item.value


It is very efficient with tables, with lots of data, and to reduce large amounts 
of memory when evaluating a QuerySet.
