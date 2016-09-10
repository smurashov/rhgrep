def non_zero(cls):
    def inner(size):
        if size <= 0:
            raise ValueError("Size can not be {}".format(size))
        return cls(size)
    return inner
