from TimeBlock import TimeBlock
class CourseSegment:
	def __init__(self):
		self.name=""
		self.prof=""
		self.room=""
		self.time_blocks = []#A list that holds every TimeBlock object for this course segment
		self.note=""
		self.eow=False

	def add (self,given_block):
		self.time_blocks.append(given_block)

	def blocks(self):
		return self.time_blocks

	def conflict_with (self,other_segment):#Check if the segment conflicts with another segment
		for block in self.time_blocks:
			for other in other_segment.blocks():
				if block.conflict_with(other):
					if not (self.eow and other_segment.eow):
						return True
		return False

	def coincident_with(self,other):
		if not len(self.time_blocks)==len(other.time_blocks):
			#If there are different numbers of blocks, they obviously aren't coincedent
			return False
		for block in self.time_blocks:
			if not block.tuple_key() in [b.tuple_key() for b in other.time_blocks]:
				#If none of the other block's tuple key matches the current block then they aren't coincedent
				return False
		return True

	def tuple_key(self):#A tuble of all the tuple keys of the time blocks
		return tuple(f.tuple_key() for f in self.time_blocks)

	def to_string(self):# Convert the Segment to a reasonably nice string
		out=""
		if self.eow:
			out+="EOW"
		for block in self.time_blocks:
			out+=block.to_string()+"\n"
		if self.room:	out+=self.room+"\n"
		if self.prof:	out+=self.prof+"\n"
		if self.note:	out+=self.note+"\n"
		return out
