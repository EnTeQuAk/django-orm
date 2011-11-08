
from django.db import models
from django_orm.postgresql import hstore

class Ref(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    _options = {
        'manager': False,
    }

class DataBag(models.Model):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField(db_index=True)

    objects = hstore.HStoreManager()
    _options = {
        'manager': False
    }

    def __unicode__(self):
        return self.name

class RefsBag(models.Model):
    name = models.CharField(max_length=32)
    refs = hstore.ReferencesField(db_index=True)

    objects = hstore.HStoreManager()

    _options = {
        'manager': False
    }

    def __unicode__(self):
        return self.name

