# -*- coding: utf-8 -*-

from django.db import models
from django_orm.postgresql.fields.arrays import ArrayField
from django_orm.postgresql.fields.interval import IntervalField
from django_orm.postgresql.fields.bytea import ByteaField
from django_orm.manager import Manager

class IntModel(models.Model):
    lista = ArrayField(dbtype='int')
    objects = Manager()
    
class TextModel(models.Model):
    lista = ArrayField(dbtype='text')
    objects = Manager()

class DoubleModel(models.Model):
    lista = ArrayField(dbtype='double precision')
    objects = Manager()

class VarcharModel(models.Model):
    lista = ArrayField(dbtype='varchar(40)')
    objects = Manager()

class IntervalModel(models.Model):
    iv = IntervalField()
    objects = Manager()

class ByteaModel(models.Model):
    bb = ByteaField()
    objects = Manager()


from django_orm.postgresql.geometric.fields import PointField, CircleField
from django_orm.postgresql.geometric.fields import LsegField, BoxField
from django_orm.postgresql.geometric.fields import PathField, PolygonField

class GeomModel(models.Model):
    pt = PointField()
    pl = PolygonField()
    ln = LsegField()
    bx = BoxField()
    cr = CircleField()
    ph = PathField()

    objects = Manager()
