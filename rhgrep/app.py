from argparse import ArgumentParser

from rhgrep.searchUtils import utils


def setup_parser():
    """Configure command line argument parser object."""
    parser = ArgumentParser(description='Find substring in file lines',
                            add_help=False)
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', nargs='*', default=['-'],
                        help='the files(s) to search')
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
    pattern = args.pattern
    files = [f if f != '-' else 'stdin' for f in args.files]

    if args.above or args.below:
        utils.grep_with_cache(
            args.files[0], pattern, args.ignore_case, args.above, args.below
        )
    else:
        utils.grep_without_cache(args.files[0], pattern, args.ignore_case)

if __name__ == '__main__':
    main()
