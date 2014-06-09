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
	
		
	def is_valid(self):
		for course1 in self.attended_segments.keys():
			for course2 in self.attended_segments.keys():
				if not course1 is course2:
					for segment1 in self.attended_segments[course1]:
						for segment2 in self.attended_segments[course2]:
							if self.courses[course1].segments[segment1].conflict_with(self.courses[course2].segments[segment2]):
								return False
		return True
		
	def score():
		return 0
		
	def pick_courses(self):
		self.recursion_depth+=1
		print("-"*self.recursion_depth+"Pick Courses")
		try: 
			pick_for=(set(self.courses.keys())-set(self.attended_segments.keys())).pop()
			types = self.unique_first_chars(self.courses[pick_for].segments.keys())
			self.pick_segments(self.courses[pick_for])
		except KeyError:#No more courses to pick for, This is the end of the tree
			print("-"*self.recursion_depth+"No courses left to pick")
			if self.is_valid():
				print("-"*self.recursion_depth+"Winner Found")
				self.winning_segments=copy.deepcopy(self.attended_segments)
				print(self.winning_segments)
		print("-"*self.recursion_depth+"End Pick Courses")
		self.recursion_depth-=1
		
		
	def unique_first_chars(self,list):
		chars=[]
		for item in list:
			chars.append(item[0])
		return set(chars)
	
	def pick_segments(self,course):
		self.recursion_depth+=1
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
			if self.is_valid():
				self.pick_courses()
		self.recursion_depth-=1