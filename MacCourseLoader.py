from bs4 import BeautifulSoup#Beautifulsoup is an HTML parser that will make parsing the schedule easier
class MacCourseLoader():
	html_file_name="Timetable.htm"
	output_file_name="stripped.txt"
	stripped_file=0
	def make_text(self,html_file_name,output_file_name):
		self.html_file_name=html_file_name
		self.output_file_name=output_file_name
		
		with open (self.html_file_name, "r") as myfile:
			html_doc=myfile.read()
			soup = BeautifulSoup(html_doc)
			stripped=soup.get_text().encode("windows-1252")#changing encoding may be needed on other platforms.
			fo = open(self.output_file_name, "wb")
			fo.write(stripped);
			# Close opened file
			fo.close()
		stripped_file=open(output_file_name, 'r')
	def read_line(self):
		return self.stripped_file.readline().strip()
	def is_course_code(self,text):
		if len(text)!=4:
			return False
		return (not text[0].isalpha())and(text[1].isalpha())and(not text[3].isalpha())
		
	def is_class_type(self,text):
		if len(text)!=3:
			return False
		return ((text[0].isalpha())and(not text[1].isalpha())and(not text[2].isalpha()))
		
	def is_room(self,text):
		return ("/" in text) and len(text)<10
	
	def is_prof(self,text):

		return ("," in text) and (text.count(" ")<=1)
	def is_time(self,text):
		if len(text)!=5 or not(":" in text[2]):
			return False
		return text.replace(":","").isnumeric()
	
	def is_section(self,text):
		return text == "DAY" or text == "EVE"
		
	def is_days(self,text):
		if len(text)<2:
			return False
		for i in range(0,len(text)-1):
			if (i%3)==2:
				if(not text[i]==" "):
					return False
			else:
				if not text[i].isalpha():
					return False
					
		return True
		
loader=MacCourseLoader()
loader.output_file_name="stripped.txt"
loader.stripped_file=open("stripped.txt", 'r')
for i in range(0,120):
	text=loader.read_line()
	if loader.is_course_code(text):
		print("Course Code:"+text)
	elif loader.is_class_type(text):
		print("Class: "+text)
	elif loader.is_room(text):
		print("Room: "+text)
	elif loader.is_prof(text):
		print("Professor: "+text)
	elif loader.is_time(text):
		print("Time: "+text)
	elif loader.is_section(text):
		print("Section: "+text)
	elif loader.is_days(text):
		print("Days: "+text)	
	else:
		print(text)