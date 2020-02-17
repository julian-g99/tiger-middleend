from parser import parse_instructions

def generate_ir(instructions, fp):
	with open(fp, 'w') as file:
		for instruction in instructions:
			if instruction.instruction_type == "function_start":
				file.write("#start_function\n")
			elif instruction.instruction_type == "function_end":
				file.write("#end_function\n\n")
			elif instruction.instruction_type == "function_int_decl":
				file.write("int-list:")
				file.write(format_variables(instruction))
			elif instruction.instruction_type == "function_float_decl":
				file.write("float-list:")
				file.write(format_variables(instruction))
			elif instruction.instruction_type == "function_def":
				file.write(instruction.argument_list[0])
			elif instruction.instruction_type == "label":
				file.write("{}:\n".format(instruction.argument_list[0]))
			else:
				file.write(normal_instruction_to_string(instruction))

def format_variables(instruction):
	result = ""
	for i in range(len(instruction.argument_list)):
		if i == 0:
			result += " " + instruction.argument_list[i]
		else:
			result += ", " + instruction.argument_list[i]
	return result + "\n"

def normal_instruction_to_string(instruction):
	result = ""
	if instruction.instruction_type == "val_assign" or instruction.instruction_type == "array_assign":
		result += "assign"
	else:
		result += instruction.instruction_type
	for arg in instruction.argument_list:
		result += ", " + arg
	return " " * 4+ result + "\n"

if __name__ == "__main__":
	instructions = parse_instructions("public_test_cases/quicksort/quicksort.ir")
	generate_ir(instructions, "quicksort.ir")
