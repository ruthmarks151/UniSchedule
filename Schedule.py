from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
import copy
from itertools import product

class Schedule():
	
	def __init__(self,courses):
		self.courses=courses#A dict of all the attended courses using the tuple keys as keys
		self.attended_segments=dict()#The dict will use the courses tuple_key as the key with the value being a tuple of the attended course segments as "C01"		
		self.winning_segments=dict()#This will hold the current winner
		self.recursion_depth=0
		self.winning_score=-10000
		
	def is_valid(self):
		for course1 in self.attended_segments.keys():
			for course2 in self.attended_segments.keys():
				if not course1 is course2:
					for segment1 in self.attended_segments[course1]:
						for segment2 in self.attended_segments[course2]:
							if self.courses[course1].segments[segment1].conflict_with(self.courses[course2].segments[segment2]):
								return False
		return True
		
	def score(self):
		score=0
		if not self.is_valid():
			return -10000
		for key in self.attended_segments.keys():
			for segment in self.attended_segments[key]:
				for i in range(1,6):
					seg=CourseSegment()
					seg.add(TimeBlock(i,8,00,9,00))
					if self.courses[key].segments[segment].conflict_with(seg):
						score-=2
		return score
			
	def pick_courses(self):
		self.recursion_depth+=1
		#print("-"*self.recursion_depth)
		pick_for=self.unpicked().pop()
		self.pick_segments(self.courses[pick_for])
		self.recursion_depth-=1
	
	def unpicked(self):
		return set(set(self.courses.keys()-self.attended_segments.keys()))
	
	def solution_found(self):
			#print(self.recursion_depth*"-"+"Root")
			if self.score()>self.winning_score:
				self.winning_segments=copy.deepcopy(self.attended_segments)
				print(self.winning_segments)
				self.winning_score=self.score()
				
	def unique_first_chars(self,list):
		chars=[]
		for item in list:
			chars.append(item[0])
		return set(chars)
	
	def pick_segments(self,course):
		segments=list(course.segments.keys())
		pick_for=self.unique_first_chars(segments)
		matrix=[]
		for type in pick_for:
			options=[]
			for segment in segments:
				if type in segment:
					options.append(segment)
			matrix.append(options)
		for combo in product(*matrix):
			self.attended_segments[course.tuple_key()]=list(combo)
			if self.unpicked():
				self.pick_courses()
			else:
				self.solution_found()
			self.attended_segments.pop(course.tuple_key(),None)