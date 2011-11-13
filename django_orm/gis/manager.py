# -*- coding: utf-8 -*-

from django_orm.postgresql.fts.mixin import SearchManagerMixIn
from django.contrib.gis.db import manager

class GeoManager(manager.GeoManager):
    use_for_related_fields = True

class FtsGeoManager(SearchManagerMixIn, manager.GeoManager):
    use_for_related_fields = True
