Low-level orm cache (beta)
==========================

Implementation of low-level cache for the django orm. It integrates with all backends supported by django-orm.

This supports this type of cache:

* Object-level cache.
* Queryset-level cache.
* Queryset-byid cache.

The **object-level** cache consists of, maintain data in memory and invalidate this if its modification.
It is used when making querys with method 'get'. And as a weak point, is that it requires you to use at 
least search by id or pk.

The **queryset-level** cache keep in memory all the queryset with all the objects it contains.

The disadvantages:

* It is necessary to evaluate fully the queryset so that it can cache.
* The invalidation of the queryset-cache only works with 'django-redis' as cache backend. 
  Otherwise, if you insert a new object, the queryset not realize until it expires.

To fill this gap, the `byid` mode in many cases it may be best solution. 
Use two queries: first, to get the ids and the second, for the objects. In this way takes a lot more the 
**object-level** cache.

In postgresql, the query is done with database-level cursors, which gives you the advantage of not 
using a lot of memory to store the list of ids! 

You can cache the first query with a `True` parameter on `byid` modifier. 
(Example: ``YourModel.objects.all().byid(True)``)


How to use this cache system?
-----------------------------

As a first step we must place as the first application ``django_orm`` in ``INSTALLED_APPS`` list. (settings.py)
This will make it automatically add some methods to the model, which allows the use of cache. 

To use the cache or other characteristic of ``django-orm`` must explicitly use the Manager of ``django-orm``.

There are also other global confuguraciones our settings can be defined but defined later.


Simple example of model
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    from django_orm.manager import Manager

    class TestModel(models.Model):
        name = models.CharField(max_length=200)
        objects = Manager()

        class OrmMeta:
            options = {
                'cache_object': True,   # enable object cache
                'cache_queryset': True, # enable queryset cache
                'default_timeout': 200, # in seconds
            }

It also has the following options to customize the operation globally on ``settings.py``:

* ``ORM_CACHE_DEFAULT_TIMEOUT`` → integer value of default cache timeout. (default 60s)
* ``ORM_CACHE_DEFAULT_ENABLED`` → boolean value for enable globaly cache (with 'manager': False you can make one exception)
* ``ORM_CACHE_KEY_PREFIX`` → set some prefix for all keys used by orm cache. (default 'orm.cache')


QuerySet reference
------------------

They have added new QuerySet methods that allow more detailed control over the cache.
You then see the reference of the new methods incorporated.

``cache(timeout=None)``
^^^^^^^^^^^^^^^^^^^^^^^

If the cache is disabled by default, this switch can only activate this queryset. You can 
specify the timeout.


``no_cache()``
^^^^^^^^^^^^^^

This parameter can disable the cache for a queryset.

``byid(cache_qs=False)``
^^^^^^^^^^^^^^^^^^^^^^^^

This parameter enables the use of another method to get the data, taking better advantage of 
cache object, without caching the whole queryset. This will make 2 querys, one to get the ids and then another to obtain 
the objects. In this way we use object cache is very fast and very simple to administer.

This parameter enables the use of another method to get the data, taking better advantage of cache object, 
without caching the whole queryset.

This will make 2 querys, one to get the ids and then another to obtain the objects.
In this way we use object cache is very fast and very simple to administer.

You can query the first cache as well, going as the first parameter to True. Consider that this has no 
effect postgresql because it uses database-level cursors.

Usage examples:
^^^^^^^^^^^^^^^

Obtain one object activating cache:

.. code-block::
    
    TestModel.objects.cache().get(pk=1)


If caching is enabled for the model, but you want, turn it off:

.. code-block::
    
    TestModel.objects.no_cache().get(pk=1)


QuerySet usage in templates:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the cache to work correctly from the templates, you use the template-tag ``withqs``. 

Here's an example of use:

.. code-block:: djangohtml
    
    {% load ormcache %}

    {% withqs posts=mypostsqueryset photos=myphotoqueryset %}
        {% for post in posts %}
        <div class="post">{{ post.content }}</div>
        {% endfor %}

        {% for photo in photos %}
        <div class="photo">{{ photo.title }}</div>
        {% endfor %}
    {% endwithqs %}

(work in progress)
