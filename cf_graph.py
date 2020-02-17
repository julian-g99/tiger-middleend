class CFGraph():
    def __init__(self, instructions, adjlist):
        self.instructions = instructions
        self.adjlist = adjlist
    
    def get_kill_set(self, iline):
        instr1 = self.instructions[iline]
        kill = []
        if not instr1.is_def:
            return kill
        for i in range(len(self.instructions)):
            instr2 = self.instructions[i]
            if instr2.is_def and instr1.does_kill(instr2):
                kill.append(instr2)
        return kill
    
    def get_predecessors(self, iline):
        predecessors = []
        for k in self.adjlist.keys():
            if iline in self.adjlist[k]:
                predecessors.append(k)
        return predecessors
    
    def remove(self, iline):
        if not (iline in self.adjlist.keys()):
            raise Exception("line number not found in cfg")
        i = 0
        while i < len(self.instructions):
            if self.instructions[i].line == iline:
                self.instructions.pop(i) #FIXME: you originally had this as iline instead of i, does this work?
            i += 1
        # for i in range(len(self.instructions)):
            # # import pdb
            # # pdb.set_trace()
            # # print("iline is:{}, instruction line is: {}".format(iline, self.instructions[i].line))
            # print("number of instructions: {}, instruction line: {}".format(len(self.instructions), i))
            # if self.instructions[i].line == iline:
                # self.instructions.pop(iline)
        self.adjlist.pop(iline) #TODO: check this
        for k in self.adjlist.keys():
            if iline in self.adjlist[k]:
                self.adjlist[k].remove(iline)


    @staticmethod
    def build(instructions):
        adjlist = {}
        for i in range(len(instructions)):
            adjlist[i] = []
        cfg = CFGraph(instructions, adjlist)
        cfg._rbuild(0, [])
        return cfg
    
    def _rbuild(self, iline, built):
        if iline < 0 or iline >= len(self.instructions):
            raise Exception("Tried to build from illegal line number: {}".format(iline))
        if iline in built:
            return
        
        built.append(iline)
        instr = self.instructions[iline]
        if instr.is_branch:
            tline = self._find_label(instr.get_branch_target())
            self.adjlist[iline].append(tline)
            self._rbuild(tline, built)
        if (not instr.is_goto) and (iline + 1 < len(self.instructions)):
            self.adjlist[iline].append(iline + 1)
            self._rbuild(iline + 1, built)
    
    def _find_label(self, label):
        for i in range(len(self.instructions)):
            instr = self.instructions[i]
            if instr.is_label and label == instr.get_label():
                return i
        return -1
    
    def display(self):
        print("=====")
        for k in self.adjlist.keys():
            print("{}: {}".format(k, self.adjlist[k]))
        print("=====")
    
    def display_verbose(self):
        print("=====")
        for k in self.adjlist.keys():
            print(self.instructions[k], end=": ")
            for i in self.adjlist[k]:
                print(self.instructions[i], end=", ")
            print()
        print("=====")

    def __str__(self):
        result = ""
        result += "Num instructions: {}\n".format(len(self.instructions))
        result += "Adjacency list: {}\n".format(self.adjlist)
        return result
