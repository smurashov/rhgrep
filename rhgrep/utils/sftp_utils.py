import fnmatch
import stat


class SftpFileSearcher:
    """
    Class for searching folders and files on remote server
    through sftp
    """

    def __init__(self, sftp):
        self.sftp = sftp

    def item_from_folder(self, folder, pattern):
        """
        Find all objects in folder
        Returns fullpath to object with id
        by id we can identify what is it(dir, file, etc.)
        """
        for name in fnmatch.filter(self.sftp.listdir(folder), pattern):
            fullpath = '{}/{}'.format(folder, name)
            mode = self.sftp.stat(fullpath).st_mode

            yield fullpath, mode

    def filenames_in_folder(self, folder, pattern='*'):
        """
        Returns names of all files in specified folder
        which satisfy to the pattern(* by default)
        """
        return (path for path, mode in self.item_from_folder(folder, pattern)
                if stat.S_ISREG(mode))

    def subfolders_in_folder(self, folder, pattern='*', recursive=False):
        """
        Returns names of all subfolders in specified folder
        which satisfy to the pattern(* by default)
        If recursive=True then retuns all subfolders with their subsubfolders
        and etc.
        This function use recursive it means that max_depth could be 200
        But it may be easily refactored to non-recursive way or we can
        do:
        import sys
        sys.setrecursionlimit(n)
        But be careful
        it can cause segmentation fault of python interpreter if n too big
        like 2^30
        """
        if not recursive:
            return [
                path for path, mode in self.item_from_folder(folder, pattern)
                if stat.S_ISDIR(mode)
            ]

        subs = []

        for path, mode in self.item_from_folder(folder, pattern):
            if stat.S_ISDIR(mode):
                subs.append(path)
                subs.extend(self.subfolders_in_folder(path,
                                                      recursive=recursive))

        return subs

    def __call__(self, filename, recursive=False):
        """
        This function is used for finding all files matching to
        the user wildcard on remote host
        """

        # split path by /
        # because user wildcard can be complex like */*/?????/*.??/[0-9].log
        # and we have to find all variants fitting to this mask
        parts = filename.split('/')

        # path can be just a simple mask like * and in this case
        # we should get list objects of parent dir
        # in this statement we define parent dir
        if filename.startswith('/'):
            parts[0] = '/'
        else:
            parts.insert(0, '.')

        paths = [parts[0]]

        # start cycle which extract all possible variants from wildcard
        for j in range(1, len(parts)):
            new_paths = []

            # the objects we are interested in are on last level of wildcard
            # in the following example: */*/?????/*.??/[0-9].log
            # it is [0-9].log
            if j == len(parts) - 1:

                # we add path if it is file which matches to the pattern
                # to finally result and if recursive=True
                # and path is folder that matches to the pattern
                # we also add all files in this folder,
                # files in subfolders, files in subsubfolders and etc.
                for path_i in paths:
                    new_paths.extend(
                        name for name in self.filenames_in_folder(
                            path_i, parts[j])
                    )

                    if not recursive:
                        continue

                    for dr in self.subfolders_in_folder(
                            path_i, parts[j], recursive=recursive):
                        new_paths.extend(self.filenames_in_folder(dr))

                return new_paths

            for path in paths:
                new_paths.extend(
                    name for name in self.subfolders_in_folder(
                        path, parts[j]
                    )
                )

            paths = new_paths