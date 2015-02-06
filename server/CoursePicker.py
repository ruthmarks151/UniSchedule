from Course import Course

class CoursePicker():
	courses=[]
	depts=set([])
	
	def __init__(self,courses):
		self.courses=courses
		for course in courses:
			self.depts.add(course.department)
	def load_file(self):
		desired_courses=dict()
		
		with open("courses.txt") as f:
			last_course_key=None
			for line in f.readlines():
				if line[0] is '(':
					arguments=line.split(",")
					#This is a really naive way of doing things and should be changed 
					for course in self.courses:
						if arguments[0].strip() in course.department:
							if arguments[1].strip() in course.code:
								if arguments[2].strip() in str(course.term):
									if course.section in arguments[3].strip():
										desired_courses[course.tuple_key()]=course
										last_course_key=course.tuple_key()
				else:
					desired_courses[last_course_key].set_segments([s.strip() for s in line.split(",")])
			
		return desired_courses
		
	def pick_course(self):
		choice = self.pick_dept()
		if choice is None:
			return None
		dept_courses=[]
		for course in self.courses:
			if course.department == choice:
				dept_courses.append(course)
		
		course_codes=[]
		print("Select the course code:")
		for course in dept_courses:
			course_codes.append(course.code)
		course_codes=list(set(course_codes))
		course_codes.sort()
		code=self.pick_any(course_codes)
		
		desired_course=[]
		for course in dept_courses:
			if course.code in code:	
				desired_course.append(course)
		index=0
		for course in desired_course:
			index=index+1
			print(str(index)+". "+self.secheduling(course))
		choice=self.get_int(index)-1
		return desired_course[choice]
		
	def pick_dept(self):
		print("Select a Department:")
		ordered_depts=sorted(list(self.depts))
		choice=self.pick_any(ordered_depts)
		return choice
	
	def pick_any(self,list):
		for index in range(0,len(list)):
			print(str(index+1)+". "+list[index])
		print("Enter the number of the desired item, 0 to cancel")
		inp=self.get_int(len(list))
		if inp==0:
			return None
		choice=list[int(inp)-1]
		return choice
		
	def get_int(self,max):
		inp=input('>>>')
		while (not inp.isdigit()) and int(inp)<=max:
			print("Please enter a number")
			inp=input('>>>')	
		return int(inp)
		
	def secheduling(self,course):
		return("Term "+str(course.term)+" "+course.section)