
import argparse
from io import IOBase

class LoadFromFile (argparse.Action):
    def __call__(self, parser, namespace, values: IOBase, option_string=None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)

def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', nargs='?',
                        default='0.0.0.0', help='default 0.0.0.0')
    parser.add_argument('--port', type=int, nargs='?',
                        default=8080, help='port to run on (default: 8080)')
    parser.add_argument('--max-points', type=int, nargs='?', default=100,
                        help='maximum number of data points stored per measurement (default: 100)')
    parser.add_argument('--cfg', type=open, action=LoadFromFile)

    return parser
