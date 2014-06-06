from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
class Course():
	def __init__(self,dept,course_code,course_name,course_term,course_section):
		self.department=dept
		self.name=course_name
		self.code=course_code
		self.term=course_term #Using McMaster's system with Semester 1 or 2 with semester 3 being both semesters
		self.section=course_section #Courses are either DAY or EVE
		self.cores=dict()
		self.labs=dict()
		self.tutorials=dict()
		
	def add(self,segment):
		if(segment.name[0]=='C'):
			self.cores.update({segment.name:segment})
		elif(segment.name[0]=='L'):
			self.labs.update({segment.name:segment})
		elif(segment.name[0]=='T'):
			self.labs.update({segment.name:segment})
		else:
			raise AssertionError
		
	def to_string(self):
		out=self.department+"\n"
		out+=self.code+"\n"
		out+=self.name+"\n"
		out+=str(self.term)+"\n"
		out+=self.section+"\n"
		for segment in self.cores:
			out+=segment+"\n"+self.cores[segment].to_string()+"\n"
		for segment in self.labs:
			out+=segment+"\n"+self.labs[segment].to_string()+"\n"
		for segment in self.tutorials:
			out+=segment+"\n"+self.tutorials[segment].to_string()+"\n"
		return out
	
	def tuple_key(self):
		return (self.department,self.code,self.term,self.section)
"""	
chem_101=Course("Chemistry","1C01","Intro To Chemistry",1,"DAY")

chem_core_1=CourseSegment("C01","Chem Prof")
chem_core_1.add(TimeBlock(1,8,00,9,00))
chem_core_1.add(TimeBlock(2,8,30,9,30))

chem_core_2=CourseSegment("C02","Chem Prof")
chem_core_2.add(TimeBlock(1,9,00,10,00))
chem_core_2.add(TimeBlock(4,8,30,9,30))

chem_lab_1=CourseSegment("L01","Lab Prof") 
chem_lab_1.add(TimeBlock(4,9,00,10,30))
chem_lab_1.add(TimeBlock(1,9,00,10,0))

chem_lab_2=CourseSegment("L02","Lab Prof") 
chem_lab_2.add(TimeBlock(4,10,00,11,00))
chem_lab_2.add(TimeBlock(5,9,00,10,0))


chem_101.add(chem_core_1)
chem_101.add(chem_core_2)
chem_101.add(chem_lab_1)
chem_101.add(chem_lab_2)

print(chem_101.to_string())
print(chem_101.tuple_key())
"""