# -*- coding: utf-8 -*-

from django.db import connection
from django.test import TestCase
from django.utils import unittest

from .models import TestModel

class UnaccentLookupTest(TestCase):
    def setUp(self):
        TestModel.objects.all().delete()
        TestModel.objects.create(name='Andréi')
        TestModel.objects.create(name='Pepê')

    def test_unaccent(self):
        qs = TestModel.objects.filter(name__unaccent='Andrei')
        self.assertEqual(qs.count(), 1)

    def test_unaccent_2(self):
        qs = TestModel.objects.filter(name__unaccent='Andrèi')
        self.assertEqual(qs.count(), 1)
