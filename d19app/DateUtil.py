import time

class DateUtil(object):
	"""docstring for DateUtil"""
	def __init__(self, arg):
		super(DateUtil, self).__init__()
		self.arg = arg
	
	@staticmethod
	def getDateDayStrFromTimeInterval(timeInterval):
		timeArray = time.localtime(timeInterval)
		dateStr = time.strftime("%Y-%m-%d", timeArray)
		return dateStr

	@staticmethod
	def getDateStrFromTimeInterval(timeInterval):

		timeArray = time.localtime(timeInterval)
		dateStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		dateStr = dateStr + " ("+ str(timeInterval) + ")"
		return dateStr