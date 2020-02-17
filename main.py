import argparse
import sys

parser = argparse.ArgumentParser(description="compiler middle end")

# file options
parser.add_argument("--input", type=str, help="File path for the input IR file")
parser.add_argument("--output", type=str, help="File path for the output IR file")

# compiler options
parser.add_argument("--dead", action="store_true", help="whether to use dead_code elim with fixed point iteration")
parser.add_argument("--copy", action="store_true", help="whether to use copy propagation")

parser.set_defaults(dead=False)
parser.set_defaults(copy=False)

args = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help(sys.stderr)
	sys.exit()
