def ge_zero(cls):
    """
    Checked that args for creating instance of class are greater or
    equal than zero
    """
    def inner(*args):
        if any((i < 0 for i in args)):
            raise ValueError("{} requires values >= 0".format(cls))
        return cls(*args)
    return inner
