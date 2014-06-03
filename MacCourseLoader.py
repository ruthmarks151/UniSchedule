#class MacCourseLoader():

from bs4 import BeautifulSoup
with open ("Timetable.htm", "r") as myfile:
	html_doc=myfile.read()
soup = BeautifulSoup(html_doc)
stripped=soup.get_text().encode("windows-1252")
fo = open("stripped.txt", "wb")
fo.write(stripped);
# Close opend file
fo.close()