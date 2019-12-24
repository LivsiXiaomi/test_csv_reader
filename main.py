import sys
from argparse import ArgumentParser, FileType

from parsing_strategies import CSVParser


def main(argv=sys.argv[1:]):
    parser = ArgumentParser(description='CSV files parser')
    parser.add_argument("filenames",
                        nargs='+',
                        help="list of files to parse")
    parser.add_argument("output_filename",
                        help="output filename")
    parser.add_argument("-f", "--format",
                        type=str,
                        dest="output_format",
                        choices=['csv', 'json', 'xml'],
                        default='csv',
                        help="output file format")

    args = parser.parse_args(argv)
    CSVParser(args.output_format, args.output_filename).parse_files(args.filenames)


if __name__ == '__main__':
    main()
