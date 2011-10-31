# -*- coding: utf-8 -*-

from django.db import connection
from django.test import TestCase
from django.utils import unittest

from .models import TestModel
from django_orm.expressions import F

class FExpressionTest(TestCase):
    def setUp(self):
        TestModel.objects.all().delete()
        TestModel.objects.create(done=False)

    def test_update(self):
        n = TestModel.objects.update(done=~F('done'))
        self.assertEqual(n, 1)
        
        obj = TestModel.objects.get()
        self.assertTrue(obj.done)

    def test_query(self):
        TestModel.objects.create(done=True, done2=False)
        TestModel.objects.create(done=True, done2=True)
        TestModel.objects.create(done=False)
        TestModel.objects.create(done=False)
        TestModel.objects.create(done=False)
        TestModel.objects.create(done=False)
        
        qs = TestModel.objects.filter(done=~F('done2'))
        self.assertEqual(qs.count(), 6)
