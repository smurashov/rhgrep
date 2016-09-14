from argparse import ArgumentParser

from rhgrep.searchUtils import utils


def setup_parser():
    """Configure command line argument parser object."""
    parser = ArgumentParser(description='Find substring in file lines',
                            add_help=False)
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('file', type=str,
                        help='the wildcard to search')
    parser.add_argument('-H', '--host', default='localhost',
                        help='address of remote host')
    parser.add_argument('-U', '--user', default='user',
                        help='username for authentication')
    parser.add_argument('-P', '--password', default='swordfish',
                        help='password for authentication')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='case-insensitive search')
    parser.add_argument('-R', '-r', '--recursive', action='store_true',
                        help='recursively search directories')
    parser.add_argument('-A', '--above', default=0, type=int,
                        help='display n lines above match')
    parser.add_argument('-B', '--below', default=0, type=int,
                        help='display n lines below match')
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    utils.ssh_grep(args.file,
                   args.pattern,
                   host=args.host,
                   user=args.user,
                   password=args.password,
                   recursive=args.recursive,
                   ignore_case=args.ignore_case,
                   above=args.above,
                   below=args.below)

if __name__ == '__main__':
    main()
