.. django-postgresql documentation master file, created by
   sphinx-quickstart on Fri Oct  7 20:59:38 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-postgresql
=================

This small project consists in maintaining a backend for django-orm, with several enhancements that will be explained below.

Due to that there are lots of different "plugins" to use different parts of postgresql are not covered by the standard orm. 
In reality this is not the problem! The problem arises when you need to use multiple orm plugins at once, and that's where 
you can not import and use!

My main motivation in creating this project is to see to unify several "plugins" in one package, so it can be used 
independently if you want one or more of them.

I certainly do not want to take all the credit, because not all the work I have done, however if you'll take care of having 
a single integrated package with a stable api.

Download: http://pypi.python.org/pypi/django-postgresql/1.6

Table of Contents:

.. toctree::
   :maxdepth: 1

   hstore/index.rst
   server-cursors.rst
   pool.rst
   aggregates.rst
   fts.rst
   fields/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

