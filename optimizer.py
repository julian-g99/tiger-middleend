from cf_graph import CFGraph
from ir_instruction import IRInstruction
from parser import get_functions
import copy

def perform_deadcode(instructions, should_print=False):
	functions = get_functions(instructions)
	cfgs = [CFGraph.build(func) for func in functions]
	optimized_instructions = []
	for cfg in cfgs:
		deadcode_elim_marksweep(cfg, should_print)
		optimized_instructions += cfg.instructions
	return optimized_instructions

def perform_copy_propagation(instructions):
	functions = get_functions(instructions)
	cfgs = [CFGraph.build(func) for func in functions]
	optimized_instructions = []
	for cfg in cfgs:
		copy_propagation(cfg)
		optimized_instructions += cfg.instructions
	return optimized_instructions

def deadcode_elim_marksweep(cfg, should_print=False):
	sets = fixed_point_iter(cfg)

	for i in range(len(cfg.instructions)):
		instruction = cfg.instructions[i]
		if instruction.instruction_type == "array_store" and instruction.argument_list[0] == 't':
			for instr2 in sets[i]["in"]:
				print(cfg.instructions[instr2])

	instructions = cfg.instructions
	worklist = []
	marked = []
	
	#mark
	for i in range(len(instructions)):
		instr = instructions[i]
		if instr.is_critical:
			worklist.append(i)
			marked.append(i)

	while len(worklist) > 0:
		i = worklist.pop()
		instr1 = instructions[i]
		for j in sets[i]["in"]:
			instr2 = instructions[j]
			if instr1.get_uses() != None and instr2.get_write_target() != None:
				if instr2.get_write_target() in instr1.get_uses():
					if not (j in marked):
						marked.append(j)
						worklist.append(j)
	
	#sweep
	# print unmarked
	# i = 0
	# while i < len(cfg.instructions):
	# for i in range(len(instructions)):
		# if i not in marked:
			# print(cfg.instructions[i])
		# i += 1

	new_instructions = [cfg.instructions[i] for i in range(len(cfg.instructions)) if i in marked]
	cfg.instructions = new_instructions
	# i = 0
	# while i < len(cfg.instructions):
	# # for i in range(len(instructions)):
		# if i not in marked:
			# # print(cfg.instructions[i].instruction_type)
			# cfg.remove(i)
		# i += 1

def copy_propagation(cfg):
	sets = fixed_point_iter(cfg)
	copies = get_all_copies(cfg)

	# instr: w = x
	# instr2: x = y
	# so we want to replace the `x` in instr with `y`
	# print(cfg.instructions[5])
	for i in range(len(cfg.instructions)):
		instr = cfg.instructions[i]
		if instr.is_use:
			for j in range(len(instr.get_uses())):
				instr_copies = get_all_copies_of(copies, instr.get_uses()[j])
				arg_copies = set([line for (target, value, line) in instr_copies])
				intersect = arg_copies.intersection(sets[i]["in"])
				only = only_copy(cfg.instructions, intersect)
				if only != None: 
					has_redef = False
					instr2 = cfg.instructions[only]
					for line_num in sets[i]["in"]:
						if cfg.instructions[line_num].is_def and cfg.instructions[line_num].get_write_target() == instr2.argument_list[1]:
							has_redef = True
					if not has_redef and (not is_constant(instr2.argument_list[1])):
						cfg.instructions[i].set_use(j, instr2.argument_list[1])

def is_constant(arg):
	try:
		float(arg)
		return True
	except ValueError:
		return False

def only_copy(instructions, intersect):
	if len(intersect) == 0:
		return None
	else:
		# first = instructions[intersect.pop()].line
		first = intersect.pop()
		for i in intersect:
			if i != first:
				return None
		return first


def get_all_copies(cfg):
	copies = set()
	# for instr in cfg.instructions:
	for i in range(len(cfg.instructions)):
		instr = cfg.instructions[i]
		if instr.instruction_type == "val_assign":
			my_tup = instr.argument_list[0], instr.argument_list[1], i
			copies.add(my_tup)
	return copies

def get_all_copies_of(copies, arg):
	instr_copies = set()
	for (target, value, line) in copies:
		if target == arg:
			instr_copies.add((target, value, line))
	return instr_copies

def fixed_point_iter(cfg):
	# print("=" * 20)
	instructions = cfg.instructions
	sets = []

	#init
	for i in range(len(instructions)):
		instr = instructions[i]
		bblock = {}
		bblock["in"] = set()
		bblock["gen"] = set() 
		if instr.is_def:
			bblock["gen"].add(i)
		bblock["kill"] = set(cfg.get_kill_set(i))
		# bblock["out"] = bblock["in"].copy()
		bblock["out"] = set()
		sets.append(bblock)

	#iterate
	change = True
	while change:
		change = False
		
		for i in range(len(instructions)):
			#calc IN
			# instr = instructions[i]
			in_set = set()
			for p in cfg.get_predecessors(i):
				in_set = in_set.union(sets[p]["out"]) #CHECK: changed here
			sets[i]["in"] = in_set
		
			#calc OUT
			# out_set = list(set(sets[i]["gen"]).union(set(in_set) - set(sets[i]["kill"])))
			out_set = sets[i]["gen"].union(in_set - sets[i]["kill"])
			# if sets[i]["out"].sort() != out_set.sort():
			if sets[i]["out"] != out_set:
				change = True
				sets[i]["out"] = out_set
	
	# print_sets(sets)
	# print("=" * 20)
	return sets


def print_sets(sets):
	for i in range(len(sets)):
		print("BB {}:".format(i))
		print("\tin: {}".format(sets[i]["in"]))
		print("\tout: {}".format(sets[i]["out"]))
		print("\tgen: {}".format(sets[i]["gen"]))
		print("\tkill: {}".format(sets[i]["kill"]))
