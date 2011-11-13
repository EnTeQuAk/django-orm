# -*- coding: utf-8 -*-


from django_orm.manager import ManagerMixIn
from django_orm.postgresql.fts.mixin import SearchManagerMixIn
from django.contrib.gis.db import manager

class GeoManager(ManagerMixIn, manager.GeoManager):
    use_for_related_fields = True

class FtsGeoManager(SearchManagerMixIn, ManagerMixIn, manager.GeoManager):
    use_for_related_fields = True
