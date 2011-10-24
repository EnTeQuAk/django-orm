# -*- coding: utf-8 -*-

from django.db import connection
from django_orm.postgresql.aggregates import Unaccent
from django.utils.unittest import TestCase

from .models import Person

class TestFts(TestCase):
    def setUp(self):
        Person.objects.all().delete()

        self.p1 = Person.objects.create(
            name=u'Andréi',
            description=u"Python programmer",
        )
        self.p2 = Person.objects.create(
            name=u'Pèpâ',
            description=u"Is a housewife",
        )

    def test_search_and(self):
        qs1 = Person.objects.search(query="programmer")
        qs2 = Person.objects.search(query="Andrei")

        self.assertEqual(qs1.count(), 1)
        self.assertEqual(qs2.count(), 1)

    def test_search_and_2(self):
        qs1 = Person.objects.search(query="Andrei & programmer")
        qs2 = Person.objects.search(query="Pepa & housewife")
        qs3 = Person.objects.search(query="Pepa & programmer")

        self.assertEqual(qs1.count(), 1)
        self.assertEqual(qs2.count(), 1)
        self.assertEqual(qs3.count(), 0)

    def test_search_or(self):
        qs1 = Person.objects.search(query="Andrei | Pepa")
        qs2 = Person.objects.search(query="Andrei | Pepo")
        qs3 = Person.objects.search(query="Pèpâ | Andrei")
        qs4 = Person.objects.search(query="Pepo | Francisco")

        self.assertEqual(qs1.count(), 2)
        self.assertEqual(qs2.count(), 1)
        self.assertEqual(qs3.count(), 2)
        self.assertEqual(qs4.count(), 0)

    def test_update_indexes(self):
        self.p1.name = 'Francisco'
        self.p1.save()

        qs = Person.objects.search(query="Pepo | Francisco")
        self.assertEqual(qs.count(), 1)
