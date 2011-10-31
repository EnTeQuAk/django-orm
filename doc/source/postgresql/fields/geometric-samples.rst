Usage examples and notes
========================

Type wrappers
-------------


Point
^^^^^

.. code-block:: python
    
    >>> from django_orm.postgresql.geometric.objects import Point
    >>> Point(2,3)
    <Point(2,3)>
    >>> Point(2,-3)
    <Point(2,-3)>


CircleField
^^^^^^^^^^^

.. code-block:: python
    
    >>> from django_orm.postgresql.geometric.objects import Circle
    >>> Circle(2,3,4)
    <Circle(<Point(2,3)>,4)>
    >>> Circle(2,3,1)
    <Circle(<Point(2,3)>,1)>


Lseg
^^^^

.. code-block:: python
    
    >>> from django_orm.postgresql.geometric.objects import Lseg
    >>> Lseg(2,3,4,5)
    <Lseg(<Point(2,3)>, <Point(4,5)>)>
    >>> Lseg((2,3),(4,5))
    <Lseg(<Point(2,3)>, <Point(4,5)>)>


Box
^^^

.. code-block:: python

    >>> from django_orm.postgresql.geometric.objects import Box
    >>> Box((2,3),(4,5))
    <Box(4,5),(2,3)>
    >>> Box(2,3,4,5)
    <Box(4,5),(2,3)>


Path
^^^^

.. code-block:: python

    >>> from django_orm.postgresql.geometric.objects import Path
    >>> Path((1,2), (3,4), (4,-2))
    <Path(3) closed=False>
    >>> Path((1,2), (3,4))
    <Path(2) closed=False>
    >>> Path((1,2), (3,4), (4,-2), (1,2), closed=True)
    <Path(4) closed=True>


Polygon
^^^^^^^

.. code-block:: python

    >>> from django_orm.postgresql.geometric.objects import Polygon
    >>> Polygon((1,2), (3,4), (4,-2))
    <Polygon(3) closed=False>
    >>> Polygon((1,2), (3,4), (4,-2), (1,2), closed=True)
    <Polygon(4) closed=True>

