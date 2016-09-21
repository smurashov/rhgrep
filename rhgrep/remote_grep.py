import paramiko

from rhgrep.utils.sftp_utils import SftpFileSearcher
import rhgrep.utils.search_utils as grep


def ssh_grep(filename,
             pattern,
             host='localhost',
             user='user',
             password='swordfish',
             recursive=False,
             ignore_case=False,
             above=0,
             below=0):
    """
    Print all necessary lines found in files on remote host
    """

    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user,
                       password=password)

        with client.open_sftp() as sftp:

            file_searcher = SftpFileSearcher(sftp)
            paths = file_searcher(filename, recursive=recursive)

            def grep_method(somefile):
                if above or below:
                    return grep.grep_with_cache(
                        somefile, pattern, ignore_case, above, below
                    )
                else:
                    return grep.grep_without_cache(
                        somefile, pattern, ignore_case
                    )

            for path in paths:
                with sftp.open(path) as file:
                    file.name = path
                    grep_method(file)
