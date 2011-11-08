# -*- coding: utf-8 -*-

from django.db import connection
from django.test import TestCase
from django.utils import unittest

from .models import TestModel
from django.core.cache import cache

class OrmCacheTest(TestCase):
    def setUp(self):
        TestModel.objects.all().delete()
        self.ob1 = TestModel.objects.create(name='A')
        self.ob2 = TestModel.objects.create(name='B')
        self.obj3 = TestModel.objects.create(name='C')
        TestModel.objects.create(name='D')
        TestModel.objects.create(name='E')
        TestModel.objects.create(name='F')
        cache.clear()

    def test_num_querys_object_cache(self):
        with self.assertNumQueries(1):
            TestModel.objects.cache().get(pk=self.ob1.id)
            TestModel.objects.cache().get(pk=self.ob1.id)
    
    def test_num_querys_object_cache_2(self):
        with self.assertNumQueries(2):
            TestModel.objects.cache().get(pk=self.ob1.id)
            TestModel.objects.cache().get(pk=self.ob1.id, name='A')

    def test_num_querys_object_cache_invalidation(self):
        with self.assertNumQueries(4):
            TestModel.objects.cache().get(pk=self.ob1.id)
            obj = TestModel.objects.cache().get(pk=self.ob1.id)
            obj.save()
            TestModel.objects.cache().get(pk=self.ob1.id)

    def test_num_querys_object_cache_3(self):
        with self.assertNumQueries(2):
            TestModel.objects.cache().get(pk=self.ob1.id)
            TestModel.objects.no_cache().get(pk=self.ob1.id)
    
    def test_num_querys_queryset(self):
        with self.assertNumQueries(1):
            a = list(TestModel.objects.cache().all())
            a = list(TestModel.objects.cache().all())

    def test_num_querys_queryset(self):
        with self.assertNumQueries(1):
            a = list(TestModel.objects.cache().exclude(name='A'))
            a = list(TestModel.objects.cache().exclude(name='A'))

    def test_num_querys_queryset_byid(self):
        with self.assertNumQueries(2):
            list(TestModel.objects.cache().all().byid(False))
            list(TestModel.objects.cache().all().byid(False))
            list(TestModel.objects.cache().all().byid(False))
            
    def test_num_querys_queryset_byid_cachedfirst(self):
        with self.assertNumQueries(2):
            list(TestModel.objects.cache().all().byid(True))
            list(TestModel.objects.cache().all().byid(True))
