from TimeBlock import TimeBlock
class CourseSegment:
	def __init__(self,given_name,given_prof=None,given_room=None):
		self.name=given_name
		self.prof=given_prof
		self.room=given_room
		self.time_blocks = []
		
	def add (self,given_block):
		self.time_blocks.append(given_block)
		
	def blocks(self):
		return self.time_blocks
	
	def conflict_with (self,other_segment):
		for block in self.time_blocks:
			for other in other_segment.blocks():
				if block.conflict_with(other):
					return True
		return False
	
	def to_string(self):
		out=""
		for block in self.time_blocks:
			out+=block.to_string()+"\n"
		if self.room:	out+=self.room+"\n"
		if self.prof:	out+=self.prof+"\n"
		return out
		
chem_core_1=CourseSegment("C01","Chem Prof")
chem_core_1.add(TimeBlock(1,8,00,9,00))
chem_core_1.add(TimeBlock(2,8,30,9,30))

math_core_1=CourseSegment("C01","Math Prof") 
math_core_1.add(TimeBlock(4,9,00,10,30))
math_core_1.add(TimeBlock(1,9,00,10,0))

math_core_2=CourseSegment("C01","Math Prof") 
math_core_2.add(TimeBlock(1,8,30,10,30))
math_core_2.add(TimeBlock(3,9,00,10,0))


if(chem_core_1.conflict_with(math_core_1)):
	print("False Positive")
	
if not (chem_core_1.conflict_with(math_core_2)):
	print("Missed Conflict")