from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
import copy

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
			self.pick_segments(self.courses[pick_for],types,[])
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
	
	def pick_segments(self,course,types,picked):
		self.recursion_depth+=1
		print("-"*self.recursion_depth+"Pick Segments")
		if not types.issubset(set()):
			pick=types.pop()
			options=[]
			for segment_key in course.segments.keys():
				if pick in segment_key:
					options.append(segment_key)
			for option in options:
				picked.append(option)
				self.pick_segments(course,types,picked)	
				picked.pop()
		else:
			if self.is_valid():
				self.attended_segments[course.tuple_key()]=picked
				self.pick_courses()
			else:
				print("-"*self.recursion_depth+"Invalid Combination")
		print("-"*self.recursion_depth+"End Pick Segments")
		self.recursion_depth-=1
		return None
		
		