__author__ = 'Aleksandr Vereshchagin'

globalCache = {}

def cached(function):
    def wrapper(*args, **kwargs):
        key = function, args, tuple(kwargs.items())
        if key in globalCache.keys():
            return globalCache[key]
        else:
            result = function(*args, **kwargs)
            globalCache[key] = result
            return result
    return wrapper
