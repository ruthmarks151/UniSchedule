class TimeBlock:
	#Define useful conversions for days of the week as global dictionaries
	#using 2 letter day abreviations Mo Tu We Th Fr
	num_to_day = {1: "Mo",
		2 : "Tu",
		3 : "We",
		4 : "Th",
		5 : "Fr",
		6 : "Sa",
	}
	day_to_num = {"Mo" : 1,
		"Tu" : 2,
		"We" : 3,
		"Th" : 4,
		"Fr" : 5,
		"Sa" : 6,
	}

	def __init__(self,day,start_time_hour,start_time_min,end_time_hour,end_time_min,term):
		try:#In case the day is given as a string, try and convert it to a number
			self.day = day_to_num[day]
		except KeyError:#It's already a number
			assert()
			self.day = day
		self.start_time_hour = start_time_hour
		self.start_time_min = start_time_min
		self.end_time_hour = end_time_hour
		self.end_time_min = end_time_min
		self.term = int(term)

	def tuple_key(self):#A tuple that represents all the timing information for the block
		return (self.day,self.start_time_hour,self.start_time_min,self.end_time_hour,self.end_time_min)

	def conflict_with(self,other_block):#Check if two timeblocks conflict with eachother
		if not (self.term==other_block.term or max([self.term,other_block.term])==3):
			return False
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

	def to_string(self):#Convert the time block to a nice string
		return self.num_to_day[self.day]+" "+str(self.start_time_hour)+":"+str(self.start_time_min)+"-"+str(self.end_time_hour)+":"+str(self.end_time_min)
