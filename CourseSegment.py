from TimeBlock import TimeBlock
class CourseSegment:
	def __init__(self):
		self.name=""
		self.prof=""
		self.room=""
		self.time_blocks = []
		self.note=""
		self.eow=False
		
	def add (self,given_block):
		self.time_blocks.append(given_block)
		
	def blocks(self):
		return self.time_blocks
	
	def conflict_with (self,other_segment):
		for block in self.time_blocks:
			for other in other_segment.blocks():
				if block.conflict_with(other):
					if not (self.eow and other_segment.eow):
						return True
		return False
	
	def to_string(self):
		out=""
		if self.eow:
			out+="EOW"
		for block in self.time_blocks:
			out+=block.to_string()+"\n"
		if self.room:	out+=self.room+"\n"
		if self.prof:	out+=self.prof+"\n"
		if self.note:	out+=self.note+"\n"
		return out
		
chem_core_1=CourseSegment()
chem_core_1.add(TimeBlock(1,8,00,9,00))
chem_core_1.add(TimeBlock(2,8,30,9,30))

math_core_1=CourseSegment() 
math_core_1.add(TimeBlock(4,9,00,10,30))
math_core_1.add(TimeBlock(1,9,00,10,0))

math_core_2=CourseSegment() 
math_core_2.add(TimeBlock(1,8,30,10,30))
math_core_2.add(TimeBlock(3,9,00,10,0))


if(chem_core_1.conflict_with(math_core_1)):
	print("False Positive")
	
if not (chem_core_1.conflict_with(math_core_2)):
	print("Missed Conflict")