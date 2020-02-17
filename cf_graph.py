class CFGraph():
    def __init__(self, instructions, adjlist):
        self.instructions = instructions
        self.adjlist = adjlist
    
    def get_kill_set(self, instr1):
        kill = []
        if not instr1.is_def:
            return kill
        for i in range(len(self.instructions)):
            instr2 = self.instructions[i]
            if instr2.is_def and instr1.does_kill(instr2):
                kill.append(instr2)
        return kill
    
    def get_predecessors(self, instr):
        predecessors = []
        for k in self.adjlist.keys():
            if instr in self.adjlist[k]:
                predecessors.append(k)
        return predecessors



    @staticmethod
    def build(self, instructions):
        adjlist = {}
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
            tline = self._find_label(instr.get_target())
            self.adjlist[iline].append(tline)
            self._rbuild(tline, built)
        if (not instr.is_goto) and (iline + 1 < len(self.instructions)):
            self.adjlist[iline].append(iline + 1)
            self._rbuild(iline + 1, built)
    
    def _find_label(self, label):
        for i in range(len(self.instructions)):
            instr = self.instructions[i]
            if instr.is_label and label == instr.get_target:
                return i
        return -1
    
    def display(self):
        print("=====")
        for k in self.adjlist.keys():
            print(k)
        print("=====")
