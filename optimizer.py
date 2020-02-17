from cf_graph import CFGraph
from ir_instruction import IRInstruction
from parser import get_functions
import copy

def perform_deadcode(instructions):
	functions = get_functions(instructions)
	cfgs = [CFGraph.build(func) for func in functions]
	optimized_instructions = []
	for cfg in cfgs:
		deadcode_elim_marksweep(cfg)
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

def deadcode_elim_marksweep(cfg):
	sets = fixed_point_iter(cfg)
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
		# for j in range(len(sets[i]["in"])):
		for j in sets[i]["in"]:
			instr2 = instructions[j]
			# print("instruction 1 is: {}, uses are: {}".format(instr1, instr.get_uses()))
			# if i == 9:
				# print("in set: {}".format(sets[i]["in"]))
				# print("out set: {}".format(sets[i]["out"]))
			# if i == 9 and j == 8:
				# print("instruction 9: {}".format(instr1))
				# print("instruction 8: {}".format(instr2))
				# print("instruction 9 uses: {}".format(instr1.get_uses()))
				# print("instruction 8 target: {}".format(instr2.get_write_target()))
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

	i = 0
	while i < len(cfg.instructions):
	# for i in range(len(instructions)):
		if not (i in marked):
			cfg.remove(i)
		i += 1

def copy_propagation(cfg):
	sets = fixed_point_iter(cfg)
	copies = get_all_copies(cfg)

	# instr: w = x
	# instr2: x = y
	# so we want to replace the `x` in instr with `y`
	for i in range(len(cfg.instructions)):
		instr = cfg.instructions[i]
		if instr.is_use:
			for j in range(len(instr.get_uses())):
				instr_copies = get_all_copies_of(copies, instr.get_uses()[j])
				arg_copies = set([line for (target, value, line) in instr_copies])
				intersect = instr_copies.intersection(sets[i]["in"])
				if len(intersect) == 1:
					has_redef = False
					instr2 = cfg.instructions[intersect.pop()]
					for line_num in sets[i]["in"]:
						if cfg.instructions[line_num].is_def and cfg.instructions[line_num].get_write_target() == instr2.argument_list[1]:
							has_redef = True
					if not has_redef:
						cfg.instructions[i].set_use(j, instr2.argument_list[1])

def get_all_copies(cfg):
	copies = set()
	for instr in cfg.instructions:
		if instr.instruction_type == "assign":
			my_tup = instr.argument_list[0], instr.argument_list[1], instr.line
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
		bblock["out"] = bblock["in"].copy()
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
