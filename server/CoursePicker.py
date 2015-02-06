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
