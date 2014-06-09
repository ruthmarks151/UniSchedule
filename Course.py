from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
class Course():
	def __init__(self,dept,course_code,course_name,course_term,course_section):
		self.department=dept
		self.name=course_name
		self.code=course_code
		self.term=course_term #Using McMaster's system with Semester 1 or 2 with semester 3 being both semesters
		self.section=course_section #Courses are either DAY or EVE
		self.segments=dict()
		
	def add(self,segment):
		self.segments[segment.name]=segment
	
	def to_string(self):
		out=self.department+"\n"
		out+=self.code+"\n"
		out+=self.name+"\n"
		out+=str(self.term)+"\n"
		out+=self.section+"\n"
		for segment in self.segments.keys():
			out+=segment+"\n"+self.segments[segment].to_string()+"\n"
		return out
	
	def tuple_key(self):
		return (self.department,self.code,self.term,self.section)
"""	
chem_101=Course("Chemistry","1C01","Intro To Chemistry",1,"DAY")

chem_core_1=CourseSegment()
chem_core_1.prof="Chem Prof"
chem_core_1.name="C01"
chem_core_1.add(TimeBlock(1,8,00,9,00))
chem_core_1.add(TimeBlock(2,8,30,9,30))

chem_core_2=CourseSegment()
chem_core_2.prof="Chem Prof"
chem_core_2.name="C02"
chem_core_2.add(TimeBlock(1,9,00,10,00))
chem_core_2.add(TimeBlock(4,8,30,9,30))

chem_lab_1=CourseSegment()
chem_lab_1.name="L01" 
chem_lab_1.add(TimeBlock(4,9,00,10,30))
chem_lab_1.add(TimeBlock(1,9,00,10,0))

chem_lab_2=CourseSegment()
chem_lab_2.name="L02"
chem_lab_2.add(TimeBlock(4,10,00,11,00))
chem_lab_2.add(TimeBlock(5,9,00,10,0))


chem_101.add(chem_core_1)
chem_101.add(chem_core_2)
chem_101.add(chem_lab_1)
chem_101.add(chem_lab_2)

print(chem_101.to_string())
"""