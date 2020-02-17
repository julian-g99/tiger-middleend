from cf_graph import CFGraph
from ir_instruction import IRInstruction

def deadcode_elim(cfg, sets):
    instructions = cfg.instructions
    worklist = []
    marked = []
    worked = []
    
    #mark
    for i in range(len(instructions)):
        instr = instructions[i]
        if instr.is_critical:
            worklist.append(i)
            marked.append(i)

    while len(worklist > 0):
        i = worklist.pop()
        instr2 = instructions[i]
        for j in range(len(sets[i]["in"])):
            instr2 = instructions[j]
            if instr2.get_write_target() in instr1.get_dependencies():
                if not (j in marked):
                    marked.append(j)
                    worklist.append(j)
    
    #sweep
    for i in range(len(instructions)):
        if not (i in marked):
            cfg.remove(i)

def fixed_point_iter(cfg):
    instructions = cfg.instructions
    sets = []

    #init
    for i in range(len(instructions)):
        instr = instructions[i]
        bblock = {}
        bblock["in"] = []
        bblock["gen"] = []
        if instr.is_def:
            bblock["gen"].append(i)
        bblock["kill"] = cfg.get_kill_set(i)
        bblock["out"] = bblock["in"]
        sets.append(bblock)

    #iterate
    change = True
    while change:
        change = False
        
        for i in range(len(instructions)):
            #calc IN
            instr = instructions[i]
            in_set = []
            for p in cfg.get_predecessors(instr):
                set(in_set).union(sets[p]["out"])
            sets[instr]["in"] = in_set
        
            #calc OUT
            out_set = list(set(sets[instr]["gen"]).union(set(in_set) - set(sets[instr]["kill"])))
            if sets[instr]["out"].sort() != out_set.sort():
                change = True
            sets[instr]["out"] = out_set
    
    return sets


def print_sets(sets):
    for i in range(len(sets)):
        print("BB {}:".format(i))
        print("\tin: {}".format(sets[i]["in"]))
        print("\tout: {}".format(sets[i]["out"]))
        print("\tgen: {}".format(sets[i]["gen"]))
        print("\tkill: {}".format(sets[i]["kill"]))
                



