# -*- coding: utf-8 -*-

from django.db import connection
from django_orm.postgresql.aggregates import Unaccent
from django.utils.unittest import TestCase

from .models import Person

class TestUnaccent(TestCase):
    def setUp(self):
        self.p1 = Person.objects.create(name='Andréi')
        self.p2 = Person.objects.create(name='Pèpâ')

    def tearDown(self):
        self.p1.delete()
        self.p2.delete()
    
    def test_annotate(self):
        qs = Person.objects.annotate(name_unaccent=Unaccent('name')).order_by('id')
        qs = list(qs)
        self.assertEqual(qs[0].name_unaccent, 'Andrei')
        self.assertEqual(qs[1].name_unaccent, 'Pepa')
