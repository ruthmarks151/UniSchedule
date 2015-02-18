from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
from MacCourseLoader import MacCourseLoader
from CoursePicker import CoursePicker
from Schedule import Schedule
from pprint import pprint

loader=MacCourseLoader()

#The stripped courses file, If it doesn't exist it'll be created
loader.output_file_name="stripped.txt"

#The HTML master timetable, that will be used to create stripped.txt
loader.html_file_name="Timetable.htm"

loader.preload()#Get ready to load all the courses

courses= [] #All courses in the master timetable
picked_courses=dict()#The courses the user actually wants to take

try:
	#Read until something throws an EOFError that means the end of the file
	while True:
		courses.append(loader.pop_course())

except EOFError:
	print("Courses loaded")

#Construct the course picker with the loaded courses
picker=CoursePicker(courses)
#Load the courses from a file
picked_courses=picker.load_file()
#Construct the schedule
schedule=Schedule(picked_courses)
#Pick the courses
schedule.pick_courses()
schedule.print_winner()
