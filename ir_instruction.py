class IRInstruction:
	def __init__(self, line, instruction_type, argument_list):
		self.line = line
		self.instruction_type = instruction_type
		self.argument_list = argument_list

		def_arr = ['val_assign',
			 'sub',
			 'add',
			 'mult',
			 'div',
			 'and',
			 'or',
			 'callr',
			 'array_load',
			 'array_assign']
		critical_arr = ['breq',
					 'brneq',
					 'brlt',
					 'brgq',
					 'brgt',
					 'brgeq',
					 'brleq',
					 'goto',
					 'function_start',
					 'function_def',
					 'function_end',
					 'function_int_decl',
					 'function_float_decl',
					 'label',
					 'call',
					 'callr',
					 'array_load',
					 'array_store',
					 'return']
		branch_arr = ['breq',
				   'brneq',
				   'brlt',
				   'brgt',
				   'brgeq',
				   'brleq',
				   'goto']

		self.is_def = self.instruction_type in def_arr
		self.is_critical = self.instruction_type in critical_arr
		self.is_branch = self.instruction_type in branch_arr
		self.is_goto = self.instruction_type == "goto"
		self.is_label = self.instruction_type == "label"

		# self.succs = []
		# self.preds = []

	def does_kill(self, other_def):
		return self.argument_list[0] == other_def.argument_list[0]

	def get_uses(self):
		binary_instructions = ['add', 'sub', 'mult', 'div', 'and', 'or']
		branches = ['breq', 'brneq', 'brlt', 'brgt', 'brgeq', 'brleq']
		if self.instruction_type == "val_assign":
			return self.argument_list[1]
		elif self.instruction_type in binary_instructions:
			return self.argument_list[1:3]
		elif self.instruction_type in branches:
			return self.argument_list[1:3]
		elif self.instruction_type == "callr":
			return self.argument_list[1:]
		elif self.instruction_type == "call":
			return self.argument_list[2:]
		elif self.instruction_type == "array_store":
			return self.argument_list[:] #NOTE: the last argument should always be a constant
		elif self.instruction_type == "array_load":
			return self.argument_list[1]
		elif self.instruction_type == "array_assign":
			return self.argument_list[:]

	def get_write_target(self):
		has_target = ['val_assign', 'array_assign', 'sub', 'add', 'mult', 'div', 'and', 'or', 'callr', 'array_load']
		if self.instruction_type in has_target:
			return self.argument_list[0].strip()

	def get_branch_target(self):
		if self.is_branch:
			return self.argument_list[0]
	
	def get_label(self):
		if self.is_label:
			return self.argument_list[0]

	
	def __str__(self):
		return "line number: {}, type: {}, argument_list: {}".format(self.line, self.instruction_type, self.argument_list)
