import rhgrep.helpers.line as myline
import rhgrep.helpers.cache as mycache


def horspul_implementation(pattern, string, ignore_case=False):
    """
    Horspool algorithm is the modification of Boyer-Moore algorithm
    it works faster then Boyer-Moore on random texts
    but slower in worst case
    I think it's enough obvious
    """
    patlen = len(pattern)
    strlen = len(string)

    if strlen < patlen:
        return -1

    if ignore_case:
        pattern, string = pattern.lower(), string.lower()

    a = []

    for i in range(256):
        a.append(patlen)

    for i in range(patlen - 1):
        a[ord(pattern[i])] = patlen - 1 - i

    a = tuple(a)
    k = patlen - 1

    while k < strlen:
        j = patlen - 1
        i = k

        while j >= 0 and string[i] == pattern[j]:
            j -= 1
            i -= 1

        if j == -1:
            return i + 1

        k += a[ord(string[k])]

    return -1


def index_find(pattern, string, ignore_case=False):
    """
    Use str.find(pattern) method
    Method which can use instead of horspool_implementation
    Use standard string.find method
    """
    if ignore_case:
        pattern, string = pattern.lower(), string.lower()
    return string.find(pattern)


def as_matched(line, pattern, index):
    """
    Mark first occurrence of pattern in string by the green color
    """
    return '{beforematch}\033[92m{match}\033[0m{aftermatch}'\
        .format(beforematch=line[:index],
                match=line[index:index + len(pattern)],
                aftermatch=line[index + len(pattern):])


def grep_without_cache(file, pattern, ignore_case):
    """
    Print to stdout all strings contained specified pattern
    """
    for num, line in enumerate(file):
        num += 1
        index = horspul_implementation(pattern, line, ignore_case)

        if index != -1:
            line = as_matched(line, pattern, index)
            print(myline.Line(line, num, file.name, match=True))


def grep_with_cache(file, pattern, ignore_case, above_size, below_size):
    """
    Print to stdout all strings contained specified pattern and
    (above) lines before match and (below) lines after match
    """

    with mycache.Cache(above_size, below_size) as cache:
        for num, line in enumerate(file):
            match = False
            num += 1
            index = horspul_implementation(pattern, line, ignore_case)

            if index != -1:
                match = True
                line = as_matched(line, pattern, index)

            line = myline.Line(
                line, num, file.name, match=match
            )
            cache.add(line)
