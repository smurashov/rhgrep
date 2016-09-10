import copy

from rhgrep.helpers.useful import non_zero


@non_zero
class SmallCache:
    def __init__(self, size):
        self.__size = size
        self.__cache = []

    def __repr__(self):
        return "\n".join(self.__cache)

    def __iter__(self):
        return iter(self.__cache)

    def __getattr__(self, item):
        return getattr(self.__cache, item)

    def append(self, item):
        if len(self.__cache) == self.__size:
            self.__cache.pop(0)
        self.__cache.append(item)

    def copy(self):
        return copy.deepcopy(self)

    def set_cache(self, cache):
        if len(cache) > self.__size:
            raise ValueError("Too big cache")
        self.__cache = cache
