# -*- coding: utf-8 -*-

import re
from django.utils import simplejson as json

rx_circle_float = re.compile(r'<\(([\d\.\-]*),([\d\.\-]*)\),([\d\.\-]*)>')
rx_line = re.compile(r'\[\(([\d\.\-]*),\s*([\w\.\-]*)\),\s*\(([\d\.\-]*),\s*([\d\.\+]*)\)\]')
rx_point = re.compile(r'\(([\d\.\-]*),\s*([\d\.\-]*)\)')
rx_box = re.compile(r'\(([\d\.\-]*),\s*([\d\.\-]*)\),\s*\(([\d\.\-]*),\s*([\d\.\-]*)\)')
rx_path_identify = re.compile(r'^((?:\(|\[))(.*)(?:\)|\])$')


class Point(object):
    """ 
    Class that rep resents of geometric point. 
    """

    x = None
    y = None
    
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1 and isinstance(args[0], (list,tuple)):
            self.x, self.y = args[0]
        self._validate()

    def _validate(self):
        if not isinstance(self.x, (int, long, float)) \
            or not isinstance(self.y, (int, long, float)):
            raise ValueError("invalid data")

    def __repr__(self):
        return "<Point(%s,%s)>" % (self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __lt__(self, val):
        return tuple(self) < tuple(val)

    def __gt__(self, val):
        return tuple(self) > tuple(val)

    def __eq__(self, val):
        return tuple(self) == tuple(val)


class Circle(object):
    point = None
    r = None

    def __init__(self, *args, **kwargs):
        if len(args) == 3:
            self.point = Point(args[:2])
            self.r = args[2]
        elif len(args) == 2:
            self.point = Point(*args[0])
            self.r = args[1]
        else:
            raise ValueError("invalid data")
        self._validate()

    def _validate(self):
        if not isinstance(self.r, (int, long, float)):
            raise ValueError("invalid data")

    def __iter__(self):
        yield self.point.x
        yield self.point.y
        yield self.r

    def __repr__(self):
        return "<Circle(%s,%s)>" % (self.point, self.r)



class Line(object):
    init_point = None
    end_point = None

    def __init__(self, *args, **kwargs):
        if len(args) == 4:
            self.init_point = Point(*args[:2])
            self.end_point = Point(*args[2:])
        elif len(args) == 2:
            self.init_point = Point(*args[0])
            self.end_point = Point(*args[1])
        else:
            raise ValueError("invalid content")

    def __iter__(self):
        yield tuple(self.init_point)
        yield tuple(self.end_point)

    def __repr__(self):
        return "<Line(%s, %s)>" % \
            (self.init_point, self.end_point)


class Lseg(Line):
    def __repr__(self):
        return "<Lseg(%s, %s)>" % \
            (self.init_point, self.end_point)


class Box(object):
    first_vertex = None
    second_vertex = None

    def __init__(self, *args, **kwargs):
        if len(args) == 4:
            self.first_vertex = Point(*args[:2])
            self.second_vertex = Point(*args[2:])
        elif len(args) == 2:
            self.first_vertex = Point(*args[0])
            self.second_vertex = Point(*args[1])
        else:
            raise ValueError("invalid content")

        self._reorder()
    
    def _reorder(self):
        if self.first_vertex < self.second_vertex:
            self.first_vertex, self.second_vertex = \
                self.second_vertex, self.first_vertex

    def __iter__(self):
        yield tuple(self.first_vertex)
        yield tuple(self.second_vertex)

    def __repr__(self):
        return "<Box(%s,%s),(%s,%s)>" % (
            self.first_vertex.x,
            self.first_vertex.y,
            self.second_vertex.x,
            self.second_vertex.y
        )

class Path(object):
    closed = False

    def __init__(self, *args, **kwargs):
        self.points = []
        for item in args:
            if isinstance(item, (tuple, list, Point)):
                self.points.append(tuple(item))
            else:
                self.points = []
                raise ValueError("invalid content")
        
        self.closed = bool(kwargs.get('closed', False))
        if len(self.points) == 0:
            raise ValueError("invalid content")
    
    def __iter__(self):
        for item in self.points:
            yield item

    def __repr__(self):
        return "<Path(%s) closed=%s>" % (len(self.points), self.closed)


class Polygon(Path):
    def __repr__(self):
        return "<Polygon(%s) closed=%s>" % (len(self.points), self.closed)


from psycopg2.extensions import adapt, register_adapter, AsIs, new_type, register_type

""" PYTHON->SQL ADAPTATION """

def adapt_point(point):
    return AsIs("'(%s, %s)'::point" % (adapt(point.x), adapt(point.y)))

def adapt_circle(c):
    return AsIs("'<(%s,%s),%s>'::circle" % \
        (adapt(c.point.x), adapt(c.point.y), adapt(c.r)))

def adapt_line(l):
    return AsIs("'[(%s,%s), (%s,%s)]'::line" % (\
        adapt(l.init_point.x),
        adapt(l.init_point.y),
        adapt(l.end_point.x),
        adapt(l.end_point.y)
    ))

def adapt_lseg(l):
    return AsIs("'[(%s,%s), (%s,%s)]'::lseg" % (\
        adapt(l.init_point.x),
        adapt(l.init_point.y),
        adapt(l.end_point.x),
        adapt(l.end_point.y)
    ))

def adapt_box(box):
    return AsIs("'(%s,%s),(%s,%s)'::box" % (
        adapt(box.first_vertex.x),
        adapt(box.first_vertex.y),
        adapt(box.second_vertex.x),
        adapt(box.second_vertex.y)
    ))

def adapt_path(path):
    container = "'[%s]'::path"
    if path.closed:
        container = "'(%s)'::path"
    
    points = ["(%s,%s)" % (x, y) \
        for x, y in path]
    return AsIs(container % (",".join(points)))


def adapt_polygon(path):
    container = "'(%s)'::polygon"
    
    points = ["(%s,%s)" % (x, y) \
        for x, y in path]

    return AsIs(container % (",".join(points)))

register_adapter(Point, adapt_point)
register_adapter(Circle, adapt_circle)
register_adapter(Line, adapt_line)
register_adapter(Box, adapt_box)
register_adapter(Path, adapt_path)
register_adapter(Polygon, adapt_polygon)
register_adapter(Lseg, adapt_lseg)

""" SQL->PYTHON ADAPTATION """

def cast_point(value, cur):
    if value is None:
        return None

    res = rx_point.search(value)
    if not res:
        raise ValueError("bad point representation: %r" % value)

    return Point([int(x) if "." not in x else float(x) \
        for x in res.groups()])


def cast_circle(value, cur):
    if value is None:
        return None

    rxres = rx_circle_float.search(value)
    if not rxres:
        raise ValueError("bad circle representation: %r" % value)

    return Circle(*[int(x) if "." not in x else float(x) \
        for x in rxres.groups()])

def cast_line(value, cur):
    if value is None:
        return None

    rxres = rx_line.search(value)
    if not rxres:
        raise ValueError("bad line representation: %r" % value)

    return Line(*[int(x) if "." not in x else float(x) \
        for x in rxres.groups()])

def cast_lseg(value, cur):
    if value is None:
        return None

    rxres = rx_line.search(value)
    if not rxres:
        raise ValueError("bad lseg representation: %r" % value)

    return Lseg(*[int(x) if "." not in x else float(x) \
        for x in rxres.groups()])

def cast_box(value, cur):
    if value is None:
        return None
    
    rxres = rx_box.search(value)
    if not rxres:
        raise ValueError("bad box representation: %r" % value)

    return Box(*[int(x) if "." not in x else float(x) \
        for x in rxres.groups()])

def cast_path(value, cur):
    if value is None:
        return None

    ident = rx_path_identify.search(value)
    if not ident:
        raise ValueError("bad path representation: %r" % value)

    is_closed = True if "(" == ident.group(1) else False
    points = ident.group(2)
    if not points.strip():
        raise ValueError("bad path representation: %r" % value)
    
    return Path(*[(
        int(x) if "." not in x else float(x), \
        int(y) if "." not in y else float(y) \
    ) for x, y in rx_point.findall(points)], closed=is_closed)

def cast_polygon(value, cur):
    if value is None:
        return None

    ident = rx_path_identify.search(value)
    if not ident:
        raise ValueError("bad path representation: %r" % value)

    is_closed = True if "(" == ident.group(1) else False
    points = ident.group(2)
    if not points.strip():
        raise ValueError("bad path representation: %r" % value)
    
    return Polygon(*[(
        int(x) if "." not in x else float(x), \
        int(y) if "." not in y else float(y) \
    ) for x, y in rx_point.findall(points)], closed=is_closed)


from django.db import connection
cur = connection.cursor()
cur.execute("SELECT NULL::point, NULL::circle, NULL::line, NULL::box, "
            "NULL::path, NULL::polygon, NULL::lseg")

point_oid, circle_oid, \
line_oid, box_oid, \
path_oid, polygon_oid, lseg_oid = \
    cur.description[0][1], \
    cur.description[1][1], \
    cur.description[2][1], \
    cur.description[3][1], \
    cur.description[4][1], \
    cur.description[5][1], \
    cur.description[6][1]

cur.close()
connection.close()

POINT = new_type((point_oid,), "POINT", cast_point)
CIRCLE = new_type((circle_oid,), "CIRCLE", cast_circle)
LINE = new_type((line_oid,), "LINE", cast_line)
BOX = new_type((box_oid,), "BOX", cast_box)
PATH = new_type((path_oid,), "PATH", cast_path)
POLYGON = new_type((polygon_oid,), "POLYGON", cast_polygon)
LSEG = new_type((lseg_oid,), "LSEG", cast_lseg)

register_type(POINT)
register_type(CIRCLE)
register_type(LINE)
register_type(BOX)
register_type(PATH)
register_type(POLYGON)
register_type(LSEG)
