def cached_property(*properties):
    def decorator(func):
        cache = {}

        def wrapper(self, *args, **kwargs):
            # Cache by object ID and provided props
            key = tuple([id(self), *[self.__dict__[prop] for prop in properties]])
            if key in cache:
                return cache[key]
            value = func(self, *args, **kwargs)
            cache[key] = value
            return value

        return property(wrapper)

    return decorator
