import paramiko
import stat
import fnmatch

import rhgrep.helpers.line as myline
import rhgrep.helpers.cache as mycache


def index_find(pattern, string, ignore_case=False):
    """
    Use str.find(pattern) method
    """
    if ignore_case:
        pattern, string = pattern.lower(), string.lower()
    return string.find(pattern)


def as_matched(line, pattern, index):
    return '{beforematch}\033[92m{match}\033[0m{aftermatch}'\
        .format(beforematch=line[:index],
                match=line[index:index + len(pattern)],
                aftermatch=line[index + len(pattern):])


def grep_without_cache(file, pattern, ignore_case):
    for num, line in enumerate(file):
        num += 1
        index = index_find(pattern, line, ignore_case)

        if index != -1:
            line = as_matched(line, pattern, index)
            print(myline.Line(line, num, file.name, match=True))


def grep_with_cache(file, pattern, ignore_case, above_size, below_size):

    with mycache.Cache(above_size, below_size) as cache:
        for num, line in enumerate(file):
            match = False
            num += 1
            index = index_find(pattern, line, ignore_case)

            if index != -1:
                match = True
                line = as_matched(line, pattern, index)

            line = myline.Line(
                line, num, file.name, match=match
            )
            cache.add(line)


def item_from_folder(sftp, folder, pattern):
    for name in fnmatch.filter(sftp.listdir(folder), pattern):
        fullpath = '{}/{}'.format(folder, name)
        mode = sftp.stat(fullpath).st_mode

        yield fullpath, mode


def filenames_in_folder(sftp, folder, pattern='*'):
    return (path for path, mode in item_from_folder(sftp, folder, pattern)
            if stat.S_ISREG(mode))


def subfolders_in_folder(sftp, folder, pattern='*', recursive=False):
    if not recursive:
        return [path for path, mode in item_from_folder(sftp, folder, pattern)
                if stat.S_ISDIR(mode)]

    subs = []

    for path, mode in item_from_folder(sftp, folder, pattern):
        if stat.S_ISDIR(mode):
            subs.append(path)
            subs.extend(subfolders_in_folder(sftp, path, recursive=recursive))

    return subs


def ssh_grep(filename,
             pattern,
             host='localhost',
             user='user',
             password='swordfish',
             recursive=False,
             ignore_case=False,
             above=0,
             below=0):

    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user,
                       password=password)

        with client.open_sftp() as sftp:
            parts = filename.split('/')

            if filename.startswith('/'):
                parts[0] = '/'
            else:
                parts.insert(0, '.')

            paths = [parts[0]]

            for j in range(1, len(parts)):
                new_paths = []

                if j == len(parts) - 1:
                    for path_i in paths:
                        new_paths.extend(
                            name for name in filenames_in_folder(
                                sftp, path_i, parts[j])
                        )

                        if not recursive:
                            continue

                        for dr in subfolders_in_folder(sftp, path_i,
                                                       parts[j],
                                                       recursive=recursive):
                            new_paths.extend(filenames_in_folder(sftp, dr))

                    paths = new_paths
                    break

                for path in paths:
                    new_paths.extend(
                        name for name in subfolders_in_folder(
                            sftp, path, parts[j]
                        )
                    )

                paths = new_paths

            def grep_method(somefile):
                if above or below:
                    return grep_with_cache(somefile, pattern, ignore_case,
                                           above, below)
                else:
                    return grep_without_cache(somefile, pattern, ignore_case)

            for path in paths:
                with sftp.open(path) as file:
                    file.name = path
                    grep_method(file)
