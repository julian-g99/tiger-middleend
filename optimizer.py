from cf_graph import CFGraph
from ir_instruction import IRInstruction

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
		for j in range(len(sets[i]["in"])):
			instr2 = instructions[j]
			# print("instruction 1 is: {}, uses are: {}".format(instr1, instr.get_uses()))
			if instr1.get_uses() != None and instr2.get_write_target() != None:
				if instr2.get_write_target() in instr1.get_uses():
					if not (j in marked):
						marked.append(j)
						worklist.append(j)
	
	#sweep
	i = 0
	while i < len(cfg.instructions):
	# for i in range(len(instructions)):
		if not (i in marked):
			cfg.remove(i)
		i += 1


def fixed_point_iter(cfg):
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
			out_set = sets[i]["gen"].union(in_set.difference(sets[i]["kill"]))
			# if sets[i]["out"].sort() != out_set.sort():
			if sets[i]["out"] != out_set:
				change = True
			sets[i]["out"] = out_set
	
	return sets


def print_sets(sets):
	for i in range(len(sets)):
		print("BB {}:".format(i))
		print("\tin: {}".format(sets[i]["in"]))
		print("\tout: {}".format(sets[i]["out"]))
		print("\tgen: {}".format(sets[i]["gen"]))
		print("\tkill: {}".format(sets[i]["kill"]))
