def get_cache_key_for_pk(model, pk, **kwargs):
    current_key = '%s:%s' % (model._meta.db_table, pk)
    if kwargs:
        current_key += ":%s" % (":".join(["%s=%s" % (k,v) for k,v in kwargs.iteritems()]))
    return current_key
