import rhgrep.helpers.line as myline
import rhgrep.helpers.cache as mycache


def index_find(pattern, string, ignore_case=False):
    """
    Use str.find(pattern) method
    """
    if ignore_case:
        pattern, string = pattern.lower(), string.lower()
    return string.find(pattern)


def display_line(filename, line_number, line):
    return '{filename}:{num}:{record}\n'.format(
        filename=filename, num=line_number, record=line)


def as_matched(line, pattern, index):
    return '{beforematch}\033[92m{match}\033[0m{aftermatch}\n'\
        .format(beforematch=line[:index],
                match=line[index:index + len(pattern)],
                aftermatch=line[index + len(pattern):])


def grep_without_cache(filename, pattern, ignore_case):
    with open(filename, 'r') as file:
        for num, line in enumerate(file):
            num += 1
            index = index_find(pattern, line, ignore_case)
            if index != -1:
                line = as_matched(line, pattern, index)
                print(myline.Line(line, num, filename, match=True))


def grep_with_cache(filename, pattern, ignore_case, above_size, below_size):

    with mycache.Cache(above_size, below_size) as cache:
        with open(filename, 'r') as file:
            for num, line in enumerate(file):
                num += 1
                index = index_find(pattern, line, ignore_case)
                match = False if index == -1 else True

                line = myline.Line(
                    as_matched(line, pattern, index), num, filename, match=match
                )
                cache.add(line)