Geometric fields
================

This is a collection of wrappers for some postgresql native geometrict types.

Currently they are implemented:

* ``django_orm.postgresql.geometric.fields.PointField``
* ``django_orm.postgresql.geometric.fields.CircleField``
* ``django_orm.postgresql.geometric.fields.LsegField``
* ``django_orm.postgresql.geometric.fields.BoxField``
* ``django_orm.postgresql.geometric.fields.PathField``
* ``django_orm.postgresql.geometric.fields.PolygonField``

and the corresponding python wrappers in the same order:

* ``django_orm.postgresql.geometric.objects.Point``
* ``django_orm.postgresql.geometric.objects.Circle``
* ``django_orm.postgresql.geometric.objects.Lseg``
* ``django_orm.postgresql.geometric.objects.Box``
* ``django_orm.postgresql.geometric.objects.Path``
* ``django_orm.postgresql.geometric.objects.Polygon``


Aggregates
----------

Currently not implemented.  But this in plans to implement:

* ``area(object) -> double``
* ``center(object) -> point``
* ``diameter(circle) -> double``
* ``height(box) -> double``
* ``isclosed(path) -> bool``
* ``isopen(path) -> bool``
* ``length(object) -> double``
* ``npoints(path, polygon)-> int``
* ``radius(circle) -> double``
* ``width(box) -> double``


QuerySet lookups
----------------

The complete list of operations on postgres geometry types here:
http://www.postgresql.org/docs/9.1/static/functions-geometry.html

With two arguments:

* ``distance``,
* ``center``,
* ``num_points``,

With one argument:

* ``is_closed``,            # isclosed(path)
* ``is_open``,              # isopen(path)
* ``length``                # length(object)
* ``length_gt``,
* ``length_lt``,
* ``length_gte``,
* ``length_lte``,
* ``width``,                # width(box)
* ``width_gt``,
* ``width_lt``,
* ``width_gte``,
* ``width_lte``,
* ``radius``,               # radius(circle)
* ``radius_gt``,
* ``radius_lt``,
* ``radius_gte``,
* ``radius_lte``,
* ``npoints``,              # npoints(path, polygon)
* ``npoints_gt``,
* ``npoints_lt``,
* ``npoints_gte``,
* ``npoints_lte``,
* ``diameter``,             # diameter(circle)
* ``diameter_gt``,
* ``diameter_lt``,
* ``diameter_gte``,
* ``diameter_lte``,
* ``center``,               # center(object)
* ``area``,                 # area(object)
* ``area_gt``,
* ``area_lt``,
* ``area_gte``,
* ``area_lte``,
* ``overlap``,
* ``strictly_left_of``,
* ``strictly_right_of``,
* ``notextendto_right_of``,
* ``notextendto_left_of``,
* ``strictly_below``,
* ``strictly_above``,
* ``notextend_above``,
* ``notextend_below``,
* ``is_below``,
* ``intersects``,
* ``is_horizontal``,
* ``is_perpendicular``,
* ``is_parallel``,
* ``contained_in_or_on``,
* ``contains``,
* ``same_as``,
