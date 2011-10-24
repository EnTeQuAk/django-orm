PostgreSQL Full Text Search
===========================

Full Text Searching (or just text search) provides the capability to identify natural-language 
documents that satisfy a query, and optionally to sort them by relevance to the query. The most 
common type of search is to find all documents containing given query terms and return them in 
order of their similarity to the query. Notions of query and similarity are very flexible and 
depend on the specific application. The simplest search considers query as a set of words and 
similarity as the frequency of query words in the document. (`From postgresql documentation.`)


Currently these classes are implemented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`django_orm.postgresql.fts.fields.VectorField`
    An tsvector index field which stores converted text into special format.

`django_orm.postgresql.fts.manager.SearchManager`
    Django manager that contains helper methods for search and re/genereate indexes.


How to use it from django?
--------------------------

To use it, you will need to add a new field and modifying one or the other method in the model.

.. code-block:: python
    
    from django_orm.postgresql.fts.manager import SearchManager
    from django_orm.postgresql.fts.fields import VectorField
    from django.db import models

    class Page(models.Model):
        name = models.CharField(max_length=200)
        description = models.TextField()

        search_index = VectorField()

        objects = SearchManager(
            fields = ('name', 'description'),
            config = 'pg_catalog.english', # this is default
            search_field = 'search_index'  # this is default
        )

        def save(self, *args, **kwargs):
            super(Page, self).save(*args, **kwargs)
            if hasattr(self, '_search_manager'):
                self._search_manager.update_index(pk=self.pk)


Notes on SearchManager usage:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The config parameter is optional and defaults to 'pg_catalog.english'.
- The fields parameter is optional. If a list of tuples, you can specify the ranking of each field, if it is None, it gets 'A' as the default.
- It can also be a simple list of fields, and the ranking will be selected by default. If the field is empty, the index was applied to all fields CharField and TextField.


To search, use the `search` method of the manager. The current version, the method used by default unaccented, so ignore the accents and searches are case insencitive.

.. code-block:: python

    >>> Page.objects.search("documentation & about")
    [<Page: Page: Home page>]
    >>> Page.objects.search("about | documentation | django | home")
    [<Page: Page: Home page>, <Page: Page: About>, <Page: Page: Navigation>]
