from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
import copy
from itertools import product
from pprint import pprint

class Schedule():
	
	def __init__(self,courses):
		self.courses=courses#A dict of all the attended courses using the tuple keys as keys
		self.attended_segments=dict()#The dict will use the courses tuple_key as the key with the value being a tuple of the attended course segments as "C01"		
		self.winning_segments=dict()#This will hold the current winner
		self.recursion_depth=0
		self.winning_score=-10000
		self.layer_sizes=dict()
		self.layer_progress=dict()
		self.last_percent=0
		self.tried_combinations=0
		self.combinations=1
		matrix=[]
		for course in courses.values():
			for type in course.coincident_segments.keys():
				options=[]
				segments=course.coincident_segments[type]
				for segment in segments.keys():
					options.append(segments[segment][0].name)
				pprint(options)
			matrix.append(options)
			self.combinations*=sum(1 for _ in product(*matrix))
					
	def is_valid(self):
		for course1 in self.attended_segments.keys():
			for segment1 in self.attended_segments[course1]:
				for segment2 in self.attended_segments[course1]:
					if not segment1 is segment2:
						if self.courses[course1].segments[segment1].conflict_with(self.courses[course1].segments[segment2]):
							return False
			for course2 in self.attended_segments.keys():
				if not course1 is course2:
					for segment1 in self.attended_segments[course1]:
						for segment2 in self.attended_segments[course2]:
							if self.courses[course1].segments[segment1].conflict_with(self.courses[course2].segments[segment2]):
								return False
		return True
		
	def score(self):
		score=0
		for key in self.attended_segments.keys():
			for i in range(1,6):
				for segment in self.attended_segments[key]:
					seg=CourseSegment()
					seg.add(TimeBlock(i,8,00,9,00,3))#Does it conflict with my appointment with sleep?
					if self.courses[key].segments[segment].conflict_with(seg):
						score-=2
					seg=CourseSegment()
					seg.add(TimeBlock(i,17,00,23,00,3))#conflict with being done at 5
					if self.courses[key].segments[segment].conflict_with(seg):
						score-=1
			for i in range(18,12):
				for segment in self.attended_segments[key]:
					seg=CourseSegment()
					seg.add(TimeBlock(5,i,00,i+1,00,3))#Does it conflict with friday plans
					if self.courses[key].segments[segment].conflict_with(seg):
						score+=2	
		return score
			
	def pick_courses(self):
		self.recursion_depth+=1
		#print("-"*self.recursion_depth)
		pick_for=self.unpicked().pop()
		self.pick_segments(self.courses[pick_for])
		self.recursion_depth-=1
	
	def print_winner(self):
		print("-*-*-Schedule-*-*-*-")
		pprint(self.winning_segments)
		print("-*-*-        -*-*-*-")
	
	def unpicked(self):
		return set(set(self.courses.keys()-self.attended_segments.keys()))
	
	def conflict_with(self,tuple_key):
		course1=tuple_key
		for segment1 in self.attended_segments[course1]:
			for segment2 in self.attended_segments[course1]:
				if not segment1 is segment2:
					if self.courses[course1].segments[segment1].conflict_with(self.courses[course1].segments[segment2]):
						return True
		for course2 in self.attended_segments.keys():
			if not course1==course2:
				for segment1 in self.attended_segments[course1]:
					for segment2 in self.attended_segments[course2]:
						if self.courses[course1].segments[segment1].conflict_with(self.courses[course2].segments[segment2]):
							return True
		return False						
				
	def solution_found(self): 
			self.tried_combinations+=1
			if self.score()>self.winning_score:
				if self.is_valid():
					pprint(self.attended_segments)
					self.winning_segments=dict(self.attended_segments)
					self.winning_score=self.score()
				
	def unique_first_chars(self,list):
		chars=[]
		for item in list:
			chars.append(item[0])
		return set(chars)
			
	def percent_complete(self):
		try:
			self.layer_progress[self.recursion_depth]+=1
		except KeyError:
			self.layer_progress[self.recursion_depth]=1
		total_progress=self.tried_combinations/self.combinations
		total_progress*=100
		if total_progress>(self.last_percent+0.1):
			print("{:.1f}".format(total_progress) +" % Complete")
			self.last_percent=total_progress
			
	def pick_segments(self,course):
		matrix=[]
		for type in course.coincident_segments.keys():
			options=[]
			segments=course.coincident_segments[type]
			for segment in segments.keys():
				options.append(segments[segment][0].name)
			matrix.append(options)
			
		try:
			self.layer_sizes[self.recursion_depth]
		except KeyError:
			self.layer_sizes[self.recursion_depth]=sum(1 for _ in product(*matrix))		
				
		for combo in product(*matrix):
			self.percent_complete()
			self.attended_segments[course.tuple_key()]=list(combo)
			if self.unpicked():
				if not self.conflict_with(course.tuple_key()):
					self.pick_courses()
				else:
					eliminated_combinations=1
					for i in range(len(self.courses),self.recursion_depth):
						eliminated_combinations*=self.layer_sizes[i]
					self.tried_combinations+=eliminated_combinations
			else:
				self.solution_found()
			self.attended_segments.pop(course.tuple_key(),None)