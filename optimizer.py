from cf_graph import CFGraph
from ir_instruction import IRInstruction


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
                



