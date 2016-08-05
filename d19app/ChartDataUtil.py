from d19app.DateUtil import DateUtil
from d19app.models import CTRecordModel
from d19app.models import CTRecordPoint
from d19app.CTLogger import CTLogger
import logging  
import logging.handlers

class ChartDataUtil(object):
	"""docstring for ChartDataUtil"""
	def __init__(self, arg):
		super(ChartDataUtil, self).__init__()
		self.arg = arg

	@staticmethod
	def getChartDataFromDBRecordsArr(recordsArr):
		timesArr = []
		standardKeys = ''
		standardKeyArr = []
		dateList = []
		resultData = {}

		logging.info("original recordsArr len:"+str(len(recordsArr)))
		for record in recordsArr:
			points = CTRecordPoint.objects.filter(fatherRecord = record).order_by("index")
			if points == None or len(points) == 0 :
				continue 
			lastKey = ''
			lastTime = 0

			keys = []
			times = []
			for point in points:
				if lastKey == '' or lastTime == 0:
					lastKey = point.key
					lastTime = float(point.timestamp)
					continue
				key = lastKey + '~' +point.key
				time = str(float(point.timestamp) - lastTime)
				lastKey = point.key
				lastTime = float(point.timestamp)
				keys.append(key)
				times.append(time)
			thisKeys = "_".join(keys)
			if standardKeys == '':
				standardKeys = "_".join(keys)
				standardKeyArr = keys
				standardKeyArr.reverse()

			# print "standardKeys: " + standardKeys + "\ncurrentKeys: " + thisKeys
			if thisKeys == standardKeys:
				times.reverse()
				timesArr.append(times)
				dateList.append(DateUtil.getDateStrFromTimeInterval(float(record.recordDate)/1000.0))
			else :
				logging.error("this key IS not equal to standard key!\nTHIS KEY:["+thisKeys+"]\nSTANDARD:["+standardKeys+"]\n")

		resultStr = "["
		resultArr = []
		for keyIndex in range(len(standardKeyArr)):
			resultItem = ''
			newTimeArr = []
			for times in timesArr:
				newTimeArr.append(times[keyIndex])
			resultItem = "{name:'"+ standardKeyArr[keyIndex] +"',data:["+",".join(newTimeArr)+"]}"
			resultArr.append(resultItem)
	
		resultStr = "[" + ",".join(resultArr) + "]"
		resultData = {"chartData":resultStr,"firstDate":DateUtil.getDateDayStrFromTimeInterval(float(recordsArr[0].recordDate)/1000.0),"dateList":dateList,"tag":recordsArr[0].recordTag}
		logging.info("return:"+str(resultData))
		return resultData

		