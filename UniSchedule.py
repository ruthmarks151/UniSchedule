from Course import Course
from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
from MacCourseLoader import MacCourseLoader
from CoursePicker import CoursePicker

loader=MacCourseLoader()
loader.output_file_name="stripped.txt"
loader.html_file_name="Timetable.htm"
loader.preload()
courses=dict()

try:
	while True:
		course=loader.pop_course()
		if course:
			courses[course.tuple_key()]=course
except EOFError:
	print("Courses loaded")
	
picker=CoursePicker(courses.values())
course=picker.pick_course()
print(course.to_string())