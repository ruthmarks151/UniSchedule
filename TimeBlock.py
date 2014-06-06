class TimeBlock:
	"""start_time_hour=0
	start_time_min=0
	end_time_hour=0
	end_time_min=0
	day=1"""
	#using 2 letter day abreviations Mo Tu We Th Fr
	num_to_day = {1: "Mo",
		2 : "Tu",
		3 : "We",
		4 : "Th",
		5 : "Fr",
	}
	day_to_num = {"Mo" : 1,
		"Tu" : 2,
		"We" : 3,
		"Th" : 4,
		"Fr" : 5,
	}
	
	def __init__(self,day,start_time_hour,start_time_min,end_time_hour,end_time_min):
		self.day=day
		self.start_time_hour=start_time_hour
		self.start_time_min=start_time_min
		self.end_time_hour=end_time_hour
		self.end_time_min=end_time_min
	
	def conflict_with(self,other_block):
		if self.day is not other_block.day:
			return False
		return max(self.start_numeric(),other_block.start_numeric())<min(self.end_numeric(),other_block.end_numeric()) 
		#If the latest start is before the earliest end there's a problem
	def to_numeric(self,hour,min):#convert a given hour and minute to the number of minutes since midnight
		return hour*60+min
		
	def start_numeric(self):#convert this time block's start time to the number of minutes since midnight
		return self.to_numeric(self.start_time_hour,self.start_time_min)
	
	def end_numeric(self):#convert this time block's end time to the number of minutes since midnight
		return self.to_numeric(self.end_time_hour,self.end_time_min)
		
	def to_string(self):
		return self.num_to_day[self.day]+" "+str(self.start_time_hour)+":"+str(self.start_time_min)+"-"+str(self.end_time_hour)+":"+str(self.end_time_min)

"""Test Cases"""		
base_case = TimeBlock(1,8,00,9,00)
conflicting =  TimeBlock(1,8,30,9,30)
almost_conflicting = TimeBlock(1,9,00,10,0)
different_day =  TimeBlock(2,8,30,9,30)

if not base_case.conflict_with(conflicting):
	print("Basic test failed")
if base_case.conflict_with(almost_conflicting):
	print("Near conflict test failed")
if base_case.conflict_with(different_day):
	print("Different day test failed")