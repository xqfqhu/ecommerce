from django.core.cache import caches
def get_query_cache_wrapper(query, query_key, timeout, cache_alias="default"):
    cache = caches[cache_alias]
    try:
        obj = cache.get(query_key)
    except:
        obj = query
    if obj is None:
        obj = query
        cache.set(query_key, obj, timeout)
    return obj

def update_query_cache_wrapper(query, query_key, timeout, cache_alias="default"):
    cache = caches[cache_alias]
    try:
        obj = cache.set(query_key, query, timeout)
    except:
        pass
        