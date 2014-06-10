from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
from MacCourseLoader import MacCourseLoader
from CoursePicker import CoursePicker
from Schedule import Schedule
from pprint import pprint

loader=MacCourseLoader()
loader.output_file_name="stripped.txt"
loader.html_file_name="Timetable.htm"
loader.preload()
courses=dict()
picked_courses=dict()

try:
	while True:
		course=loader.pop_course()
		if course:
			courses[course.tuple_key()]=course
except EOFError:
	print("Courses loaded")
	
picker=CoursePicker(courses.values())
"""course=picker.pick_course()
while course:
	print("Adding \n"+course.to_string()+"to your schedule")
	picked_courses[course.tuple_key()]=course
	course=picker.pick_course()"""
picked_courses=picker.load_file()
schedule=Schedule(picked_courses)
print(schedule.courses)
schedule.pick_courses()
schedule.print_winner()