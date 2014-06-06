from bs4 import BeautifulSoup#Beautifulsoup is an HTML parser that will make parsing the schedule easier
from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock

class MacCourseLoader():
	html_file_name="Timetable.htm"
	output_file_name="stripped.txt"
	stripped_file=None
	current_dept=None
	peeked_line=False
	
	def preload(self):
		try:
			self.stripped_file=open(self.output_file_name, 'r')
		except:
			self.make_text(self.html_file_name,self.output_file_name)
		self.stripped_file=open(self.output_file_name, 'r')

		for i in range(0,2):#there are 10 lines before the first department
			self.read_line()
	
	def pop_course(self):
		line=self.read_line()
		if self.is_dept(line):
			self.current_dept=line
			line=self.read_line()		
		course_code=line
		assert self.is_course_code(course_code)
		course_name=self.read_line()
		line=self.read_line()
		if line=="NOT OFFERED":
			return None
		course_term=int(line[len(line)-1])
		course_section=self.read_line()
		assert self.is_section(course_section)
		new_course=Course(self.current_dept,course_code,course_name,course_term,course_section)
		if "EOW" in self.peek_line() or "SITE STUDENTS" in self.peek_line():
				self.read_line()
		if "CANCELLED" in self.peek_line():
			while not (self.is_course_code(self.peek_line()) or self.is_dept(self.peek_line())):
				self.read_line()
			return None
		else:	
			while self.is_class_type(self.peek_line()):
				new_course_segment=self.read_course_segment()
				if new_course_segment:
					new_course.add(new_course_segment)
				if "EOW" in self.peek_line() or "SITE STUDENTS" in self.peek_line():
					self.read_line()
		return new_course
		
	def read_course_segment(self):
		segment_name=self.read_line()
		if "EOW" in segment_name:
			segment_name=self.read_line()
		assert self.is_class_type(segment_name)
		if "TBA" in self.peek_line():
			while not (self.is_course_code(self.peek_line()) or self.is_class_type(self.peek_line()) or self.is_dept(self.peek_line())):
				self.read_line()
			return None
		new_segment=CourseSegment(segment_name)
		while self.is_days(self.peek_line()):
			line=self.read_line()
			assert self.is_days(line)
			days=line.split()
			
			start_hour,start_min=self.read_time()
			end_hour,end_min=self.read_time()
			
			for day in days:
				block=TimeBlock(TimeBlock.day_to_num[day],start_hour,start_min,end_hour,end_min)
				new_segment.add(block)
			term=self.read_line()
			line=self.peek_line()
			if self.is_room(line):
				new_segment.room=self.read_line()
				line=self.peek_line()
			if self.is_prof(line):
				new_segment.prof=self.read_line()
				line=self.peek_line()
			if  not (self.is_course_code(line) or self.is_dept(line) or self.is_days(line) or self.is_class_type(line)):#self.is_added_message(self.peek_line()):
				line=self.read_line()
		return new_segment
		
	def read_time(self):
		line=self.read_line()
		assert self.is_time(line)
		hour,min=line.split(":")
		hour=int(hour)
		min=int(min)
		return hour,min	
	
	def make_text(self,html_file_name,output_file_name):
		self.html_file_name=html_file_name
		self.output_file_name=output_file_name
		
		with open (self.html_file_name, "r") as myfile:
			html_doc=myfile.read()
			soup = BeautifulSoup(html_doc)
			stripped=soup.get_text().encode("windows-1252")#changing encoding may be needed on other platforms.
			fo = open(self.output_file_name, "wb")
			fo.write(stripped)
			# Close opened file
			fo.close()
		
		self.stripped_file=open(output_file_name, 'r')
		
	def peek_line(self):#Reads the the next line in the file but stores it as peekedline
		self.peeked_line=self.read_line()
		return self.peeked_line
	def read_line(self):#returns the next non blank line in the file, unless a line was peeked, then it returns the peeked line.
		if self.peeked_line:
			line=self.peeked_line
			self.peeked_line=False
		else:
			line=self.stripped_file.readline()
			if not line:
				raise EOFError()
			line=str(line).strip()
			while line=="":
				line=self.stripped_file.readline()
				if not line:
					raise EOFError()
				line=str(line).strip()
		return line
		
	def is_course_code(self,text):
		if len(text)!=4:
			return False
		return (not text[0].isalpha())and(text[1].isalpha())and(not text[3].isalpha())		
	def is_class_type(self,text):
		if not len(text)==3:
			return False
		return ((text[0].isalpha())and(not text[1].isalpha())and(not text[2].isalpha()))		
	def is_room(self,text):
		if "MHK/CAMPUS" in text or "CON/CAMPUS" in text:
			return True
		return ("/" in text) and len(text)<10
	def is_prof(self,text):
		return ("," in text) and (text.count(" ")<=5)
	def is_time(self,text):
		if len(text)!=5 or not(":" in text[2]):
			return False
		return text.replace(":","").isnumeric()
	def is_section(self,text):
		return text == "DAY" or text == "EVE"		
	def is_days(self,text):
		words=text.split()
		for word in words:
			if not word in TimeBlock.day_to_num:
				return False
		return True
	def is_dept(self,text):
		depts=[
			"ANTHROPOLOGY (ANTHROP)",
			"ART (ART)",
			"ART HISTORY (ART HIST)",
			"ARTS & SCIENCE (ARTS&SCI)",
			"ASTRONOMY (ASTRON)",
			"WOMEN'S STUDIES (WOMEN ST)"]
		for dept in depts:
			if dept.lower() in text.lower():
				return True
		return False	
	def is_dept(self,text):
		return "(" in text and ")" in text
			
	
loader=MacCourseLoader()
loader.output_file_name="stripped.txt"
loader.html_file_name="Timetable.htm"
loader.preload()
courses=[]
try:
	while true:
		course=loader.pop_course()
		if course:
			courses.append(course)
			print(course.to_string())
		print("--------------------")
except EOFError:
	print("End of file!")
	