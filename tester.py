from parser import parse_instructions, get_functions
from cf_graph import CFGraph
from ir_generation import generate_ir
from ir_instruction import IRInstruction
from optimizer import perform_deadcode, perform_copy_propagation



def test_quicksort():
	instructions = parse_instructions("public_test_cases/quicksort/quicksort.ir")
	# instructions = parse_instructions("public_test_cases/sqrt/sqrt.ir")

	first_pass = perform_deadcode(instructions)
	generate_ir(first_pass, "first_pass.ir")
	first_pass = parse_instructions("first_pass.ir")

	second_pass = perform_copy_propagation(first_pass)
	generate_ir(second_pass, "second_pass.ir")
	second_pass = parse_instructions("second_pass.ir")

	final = perform_deadcode(second_pass)
	generate_ir(final, "final.ir")

def test_set_use():
	instruction = IRInstruction(0, "val_assign", ["x", "y"])
	print(instruction)
	instruction.set_use(0, "z")
	print(instruction)

def main():
	test_quicksort()
	# test_set_use()


if __name__ == '__main__':
	main()
