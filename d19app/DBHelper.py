#coding:utf-8
from d19app.models import CTRUser
from d19app.models import CTRecordModel
from d19app.models import CTRecordPoint
from d19app.HTTPUtil import HTTPRSPCode
from d19app.DateUtil import DateUtil

class DBHelper(object):
	"""docstring for DBHelper"""
	def __init__(self, arg):
		super(DBHelper, self).__init__()
		self.arg = arg

	@staticmethod
	def saveRecordsByData(userName, records):

		errCode = HTTPRSPCode.OK
		errMsg = "ok"
		if not userName or not records:
			errCode = HTTPRSPCode.INVALID_PARAMS
			errMsg = "userName and records required"
		else :
			user,created = CTRUser.objects.get_or_create(userName=userName)
			user.save()
			if created:
				print "user created:" + str(user)
			else:
				print "user found:" + str(user)
		
			for record in records:
				if not (record.has_key('recordTag') and record.has_key('recordDate') and record.has_key('points')):
					continue
				recordTag = record['recordTag']
				recordDate = record['recordDate']
				points = record['points']
				recordDateDayStr = DateUtil.getDateDayStrFromTimeInterval(float(recordDate)/1000.0)
				if recordTag == None or recordDate == None or points == None:
					continue
		 		tempCode,tempMsg = CTRecordModel.createAndSaveRecord(user,recordTag,recordDate,recordDateDayStr,points)
				if tempCode != 0:
					errCode = tempCode
					errMsg = tempMsg
		if errCode == 0:
			print "RECORDS SAVE TASK SUCCESS!"
		else:
			print "ERR AT SAIVNG TASK:" + errMsg

		return errCode,errMsg