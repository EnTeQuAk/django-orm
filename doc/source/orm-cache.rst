Low-level orm cache (beta)
==========================

Implementation of low-level cache for the django orm. It integrates with all backends supported by django-orm.


Features:
---------

* Object-level cache.
* Queryset-level cache.


How to use this cache system?
-----------------------------

As a first step we must place as the first application django_orm.cache in INSTALLED_APPS list. (settings.py)

This will make it automatically assign a manager to the model, which allows the use of cache. The automatic 
assignments are flexible and can be configured through the attribute _options we add to the model.

There are also other global confuguraciones our settings can be defined but defined later.


Simple example of model.
^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        _options = {
            'manager': True,        # automaticaly add manager to 'objects' attr
                                    # you can change this by putting the name, instead of the True
            'cache_object': True,   # enable object cache
            'cache_queryset': True, # enable queryset cache
            'default_timeout': 200, # in seconds
        }

It also has the following options to customize the operation globally on ``settings.py``:

* ``ORM_CACHE_DEFAULT_TIMEOUT`` → integer value of default cache timeout. (default 60s)
* ``ORM_CACHE_DEFAULT_ENABLED`` → boolean value for enable globaly cache (with 'manager': False you can make one exception)
* ``ORM_CACHE_DEFAULT_ADD_MANAGET`` → boolean value for set globaly insert manager. (default True)
* ``ORM_CACHE_DEFAULT_MANAGER_ALIAS`` → str value for set the default alias for automatic manager assignation. (default 'objects')
* ``ORM_CACHE_KEY_PREFIX`` → set some prefix for all keys used by orm cache. (default 'orm.cache')
* ``ORM_CACHE_FETCH_BY_ID`` → flat for set other method for obtain objects. Make better use of the cache object. (default False)

(work in progress)
