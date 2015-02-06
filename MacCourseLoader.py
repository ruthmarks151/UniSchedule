from bs4 import BeautifulSoup#Beautifulsoup is an HTML parser that will make parsing the schedule easier
from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock

class MacCourseLoader():
	html_file_name="Timetable.htm"  #redundant, UniSchedule.py assigns same value
	output_file_name="stripped.txt" #redundant, UniSchedule.py assigns same value
	stripped_file=None
	current_dept=None
	peeked_line=False
	line_no=0
	
	
	def pop_course(self):
		#Reads one course from file
		#returns None if course isn't scheduled for this year
		#Otherwise gives course
		
		line=self.read_line()
		
		#Occasionally instead of a course's information a line will have a new
		#department, if this is the case set the department to the current line
		#and then read in another line which should be a course code
		if self.is_dept(line):
			self.current_dept=line
			line=self.read_line()	
			
		course_code=line

		if not self.is_course_code(course_code):
			print(course_code)
			print(self.line_no)
		assert self.is_course_code(course_code)
		
		course_name=self.read_line()
		
		line=self.read_line()
		if line in "NOT OFFERED":#This exact string is used to indicate not offered courses
			return None
		course_term=int(line[-1])#Get the last character of the line, "T1" -> 1
		
		course_section=self.read_line()#DAY or NIGHT are the exact strings
		assert self.is_section(course_section)
		
		#All of the course's information has been loaded so the course is created
		new_course=Course(self.current_dept,course_code,course_name,course_term,course_section)
		
		#If information about what site the course is for is given, it is skipped over
		if "SITE STUDENTS" in self.peek_line():
				self.read_line()
				
		#If the course is cancelled read ahead until the next line is a course or a department
		if "CANCELLED" in self.peek_line():
			while not (self.is_course_code(self.peek_line()) or self.is_dept(self.peek_line())):
				self.read_line()
			return None
		
		#Read in all of the courses segments
		while (self.is_class_type(self.peek_line()) or 
				"EOW" in self.peek_line() or 
				"CANCELLED" in self.peek_line() or 
				"SITE" in self.peek_line()):

			new_course_segment=self.read_course_segment()
			if new_course_segment:
				new_course.add(new_course_segment)
			if "EOW" in self.peek_line() or "SITE" in self.peek_line():
				self.read_line()
		new_course.consolidate_courses()
		return new_course
		
	def read_course_segment(self):
		#Reads one course segment
		#Ensures the course is running
		#Gets the note if any
		new_segment=CourseSegment()
		line=self.read_line()
		
		
		if "EOW" in line:
			new_segment.eow=True
			line=self.read_line()
		
		if "CANCELLED" in line:
			while not (self.is_course_code(self.peek_line()) or
					   self.is_class_type(self.peek_line()) or 
					   self.is_dept(self.peek_line())):
				self.read_line()
			return None

		assert self.is_class_type(line)
		new_segment.name=line

		if "TBA" in self.peek_line() or "CANCELLED" in self.peek_line():
			while not (self.is_course_code(self.peek_line()) or 
						self.is_class_type(self.peek_line()) or 
					 	self.is_dept(self.peek_line())):

				self.read_line()
			return None

		while self.is_days(self.peek_line()):
			line=self.read_line()
			assert self.is_days(line)
			days=line.split()
			
			start_hour,start_min=self.read_time()
			end_hour,end_min=self.read_time()
			term=int(self.read_line())
			
			for day in days:
				block=TimeBlock(TimeBlock.day_to_num[day],start_hour,start_min,end_hour,end_min,term)
				new_segment.add(block)
			
			line=self.peek_line()
			if self.is_room(line):
				new_segment.room=self.read_line()
				line=self.peek_line()
			if self.is_prof(line):
				new_segment.prof=self.read_line()
				line=self.peek_line()
			if self.is_note(line):
				new_segment.note=self.read_line()
		return new_segment
			
	def read_time(self):
		line=self.read_line()
		assert self.is_time(line)
		hour,min=line.split(":")
		hour=int(hour)
		min=int(min)
		return hour,min	
	
	def make_text(self,html_file_name,output_file_name):
		#Open HTML
		#Scrape it with beautiful soup
		#write out to a file
		self.html_file_name=html_file_name
		self.output_file_name=output_file_name
		
		with open (self.html_file_name, "r") as myfile:
			html_doc=myfile.read()
			soup = BeautifulSoup(html_doc)
			stripped=soup.get_text().encode("ascii",'ignore')#changing encoding may be needed on other platforms.
			fo = open(self.output_file_name, "wb")
			fo.write(stripped)
			# Close opened file
			fo.close()
		
		self.stripped_file=open(output_file_name, 'r')
		
	def preload(self):
		#Try to open file
		#if it does not exist yet
		#make it, prep to read
		try:
			self.stripped_file=open(self.output_file_name, 'r')
		except:
			self.make_text(self.html_file_name,self.output_file_name)
            self.stripped_file=open(self.output_file_name, 'r')

		for i in range(0,2):#there are 10 lines before the first department
			self.read_line()
			
	def peek_line(self):#Reads the the next line in the file but stores it as peekedline
		self.peeked_line=self.read_line()
		return self.peeked_line

	def read_line(self):#returns the next non blank line in the file, unless a line was peeked, then it returns the peeked line.
		if self.peeked_line:
			line=self.peeked_line
			self.peeked_line=False
		else:
			line=self.stripped_file.readline()
			self.line_no+=1
            if line == "":#An empty string indicates EOF
				raise EOFError()
			line=str(line).strip()#Strip whitespace from the read line
            while line=="":#If the line was just whitespace
				self.line_no+=1
				line=self.stripped_file.readline()
				if line == "":#An empty string indicates EOF
					raise EOFError()
                
				line=str(line).strip()#Strip whitespace and newlines
		return line
		
	def is_note(self,text):
		#list other methods
		#iterate and try them all
		#woo hoo go python
		other_checks=[
			self.is_course_code,
			self.is_class_type,
			self.is_section,
			self.is_days,
			self.is_dept,]
		for check in other_checks:
			if check(text):
				return False
		return True
		
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

		return "(" in text and ")" in text
		