from rhgrep.helpers.useful import ge_zero


@ge_zero
class Cache:
    def __init__(self, above, below):
        self.above_cache = []
        self.__above = above
        self.__below = below
        self.__cache = []
        self.__match_line = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def add(self, item):
        if item.match:
            self.__match_line = item
            self.__cache.extend(filter(lambda x: x not in self.__cache,
                                       self.above_cache))
        if not self.__match_line and self.__above:
            self._add_to_above_cache(item)
            return
        elif self.__match_line and self.__match_line.num + self.__below >=\
                item.num:
            self.__cache.append(item)
            return
        if self.__above:
            self.__match_line = None
            self.above_cache = self.__cache[-self.__above:]
            self._add_to_above_cache(item)

    def _add_to_above_cache(self, item):
        if len(self.above_cache) == self.__above:
            self.above_cache.pop(0)
        self.above_cache.append(item)

    def release(self):
        print('\n'.join(map(str, self.__cache)))
        self.__cache = []