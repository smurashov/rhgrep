from rhgrep.helpers.useful import ge_zero


@ge_zero
class Cache:
    """
    Cache contains two parts: __cache and above_cache
    __cache - main part of cache which comprises main part of cache.
        Lines for print are conserved in this cache

    above_cache - contains only 'above' number of line before the next
        match

    __below - number of lines to preserve after match

    __match_line - the last matched line until current number of line
        is less than __below, otherwise it's None

    Cache support context manager interface
    Cache ensure that we keep only necessary lines without duplicates
    For example in case when we have 100 matches of pattern, and we have to
    print also 500 lines above and 500 lines below it's difficulty to
    preserve all 50000 lines in the same time this lines can duplicate
    each other and we ensure that we will print only unique lines
    """
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
        """
        Add line to cache.
        """
        # If we get match of pattern in current line
        # we set __match_line = current line and add above_cache to cache
        if item.match:
            self.__match_line = item
            self.__cache.extend(filter(lambda x: x not in self.__cache,
                                       self.above_cache))

        # if so far we don't get any matches or '__below' lines after
        # last match were saved in main cache
        # we add new one to above_cache
        if not self.__match_line and self.__above:
            self._add_to_above_cache(item)
            return

        # if we recently get match of pattern and don't meet another match
        # and at the same time size of lines below match are great than
        # current line number we add it to main cache
        elif self.__match_line and self.__match_line.num + self.__below >=\
                item.num:
            self.__cache.append(item)
            return

        # if we came to this condition it's mean only one
        # to wit that we save enough lines(__below) after last match
        # and we don't need to preserve more lines
        # set match_line to None and replace current above_cache
        # by the last (__above) lines of main cache
        # and add new one to __above_cache
        if self.__above:
            self.__match_line = None
            self.above_cache = self.__cache[-self.__above:]
            self._add_to_above_cache(item)

    def _add_to_above_cache(self, item):
        """
        Add element to above_cache
        Check if len of above_cache is equal to self.__above if so
        remove first element of above_cache and add new one to the end
        """
        if len(self.above_cache) == self.__above:
            self.above_cache.pop(0)
        self.above_cache.append(item)

    def release(self):
        """
        Print all lines and set cache to emtpy list
        """
        print('\n'.join(map(str, self.__cache)))
        self.__cache = []