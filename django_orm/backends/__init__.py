# -*- coding: utf-8 -*-

from django.dispatch import receiver
from django.db.backends.signals import connection_created

@receiver(connection_created)
def my_callback(sender, connection, signal, **kwargs):
    #print "Connection created:", id(connection.connection)
    pass
