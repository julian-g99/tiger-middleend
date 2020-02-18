import argparse
import sys
from parser import parse_instructions, get_functions
from cf_graph import CFGraph
from ir_generation import generate_ir
from ir_instruction import IRInstruction
from optimizer import perform_deadcode, perform_copy_propagation

parser = argparse.ArgumentParser(description="compiler middle end")

# file options
parser.add_argument("--input", type=str, help="File path for the input IR file", required=True)
parser.add_argument("--output", type=str, help="File path for the output IR file", required=True)

# compiler options
parser.add_argument("--dead", action="store_true", help="whether to use dead_code elim with fixed point iteration")
parser.add_argument("--copy", action="store_true", help="whether to use copy propagation")

parser.set_defaults(dead=False)
parser.set_defaults(copy=False)

args = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help(sys.stderr)
	sys.exit()

def main():
	instructions = parse_instructions(args.input)

	if args.dead and args.copy:
		first_pass = perform_deadcode(instructions)
		generate_ir(first_pass, "outputs/first_pass.ir")
		first_pass = parse_instructions("outputs/first_pass.ir")

		second_pass = perform_copy_propagation(first_pass)
		generate_ir(second_pass, "outputs/second_pass.ir")
		second_pass = parse_instructions("outputs/second_pass.ir")

		final = perform_deadcode(second_pass)
		generate_ir(final, args.output)
	elif args.dead:
		final = perform_deadcode(instructions)
		generate_ir(final, args.output)
	elif args.copy:
		final = perform_copy_propagation(instructions)
		generate_ir(final, args.output)
	else:
		generate_ir(instructions, args.output)



if __name__ == "__main__":
	main()
