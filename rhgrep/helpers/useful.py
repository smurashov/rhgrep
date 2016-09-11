def ge_zero(cls):
    def inner(*args):
        if any((i < 0 for i in args)):
            raise ValueError("{} requires values >= 0".format(cls))
        return cls(*args)
    return inner
