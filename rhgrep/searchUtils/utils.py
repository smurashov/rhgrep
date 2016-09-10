import sys

import rhgrep.helpers.SmallCache as scache


def index_find(pattern, string, ignoreCase=False):
    """
    Use str.find(pattern) method
    """
    if ignoreCase:
        pattern, string = pattern.lower(), string.lower()
    return string.find(pattern)


def display_line(filename, line_number, line):
    return '{filename}:{num}:{record}\n'.format(
        filename=filename, num=line_number, record=line)


def grep_file(filename, pattern, ignore_case, above_size, below_size):
    with open(filename, 'r') as file:
        num = 0
        cache = []
        above_cache = scache.SmallCache(above_size) if above_size else []
        match_index = 0

        for line in file:
            num += 1
            index = index_find(pattern, line, ignore_case)
            if index != -1:
                line = '{beforematch}\033[92m{match}\033' \
                       '[0m{aftermatch}\n'\
                    .format(beforematch=line[:index],
                            match=line[index:index + len(pattern)],
                            aftermatch=line[index + len(pattern):])

                if not (above_size or below_size):
                    sys.stdout.write(display_line(filename, num, line))
                    continue

                match_index = num
                cache.extend(filter(lambda x: x not in cache, above_cache))

            if match_index == 0 and above_cache:
                above_cache.append(display_line(filename, num, line))
            elif match_index != 0 and num <= match_index + below_size:
                cache.append(display_line(filename, num, line))
            elif above_cache:
                above_cache.set_cache(cache[-above_size:])
                above_cache.append(display_line(filename, num, line))
                match_index = 0

    for val in cache:
        sys.stdout.write(val)
