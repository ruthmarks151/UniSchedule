from TimeBlock import TimeBlock
class CourseSegment:
	def __init__(self,given_name):
		self.name=given_name
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

chem_core_1=CourseSegment("C01")
chem_core_1.add(TimeBlock(1,8,00,9,00))
chem_core_1.add(TimeBlock(2,8,30,9,30))

math_core_1=CourseSegment("C01") 
math_core_1.add(TimeBlock(4,9,00,10,30))
math_core_1.add(TimeBlock(1,9,00,10,0))

math_core_2=CourseSegment("C01") 
math_core_2.add(TimeBlock(1,8,30,10,30))
math_core_2.add(TimeBlock(3,9,00,10,0))


if(chem_core_1.conflict_with(math_core_1)):
	print("False Positive")
	
if not (chem_core_1.conflict_with(math_core_2)):
	print("Missed Conflict")