# -*- coding: utf-8 -*-

from django.db.models.sql.constants import QUERY_TERMS

QUERY_TERMS.update(dict([(x, None) for x in ['unaccent', 'iunaccent']]))
