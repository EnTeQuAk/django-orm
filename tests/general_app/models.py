# -*- coding: utf-8 -*-

from django.db import models
from django_postgresql.fields.arrays import ArrayField
from django_postgresql.fields.interval import IntervalField
from django_postgresql.fields.bytea import ByteaField
from django_postgresql.manager import PgManager

class IntModel(models.Model):
    lista = ArrayField(dbtype='int')
    objects = PgManager()
    
class TextModel(models.Model):
    lista = ArrayField(dbtype='text')
    objects = PgManager()

class DoubleModel(models.Model):
    lista = ArrayField(dbtype='double precision')
    objects = PgManager()

class VarcharModel(models.Model):
    lista = ArrayField(dbtype='varchar(40)')
    objects = PgManager()

class IntervalModel(models.Model):
    iv = IntervalField()
    objects = PgManager()

class ByteaModel(models.Model):
    bb = ByteaField()
    objects = PgManager()


from django_postgresql.geometric.fields import PointField, CircleField
from django_postgresql.geometric.fields import LsegField, BoxField
from django_postgresql.geometric.fields import PathField, PolygonField

class GeomModel(models.Model):
    pt = PointField()
    pl = PolygonField()
    ln = LsegField()
    bx = BoxField()
    cr = CircleField()
    ph = PathField()

    objects = PgManager()
