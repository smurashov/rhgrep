class Line:
    def __init__(self, string, num, filename, match=False):
        self.string = string
        self.num = num
        self.filename = filename
        self.match = match

    def __repr__(self):
        return '{filename}:{num}:{record}\n'.format(
            filename=self.filename, num=self.num, record=self.string
        )

    def __str__(self):
        return self.__repr__()