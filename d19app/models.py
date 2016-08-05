#coding:utf-8
from django.db import models
from datetime import datetime
from django.utils import timezone

import types

# Create your models here.

#User表
class CTRUser(models.Model):

	#id 用户id
	#userId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	userId = models.AutoField(primary_key = True)
	#用户名 不为空
	userName = models.CharField(max_length = 32)
	#密码 可为空
	password = models.CharField(max_length = 128, blank = True, null = True)
	#邮件 可为空
	Email = models.EmailField(blank = True, null = True)
	#注册日期 自动插入创建日期
	registerDate = models.DateTimeField(auto_now_add = True) 
	#上次登录日期 默认为首次创建时间
	lastLoginDate = models.DateTimeField(default = timezone.now, blank = True, null = True)

	def __unicode__(self):
		return str(self.userId) +" "+ self.userName;
		

#CTRModel表:单条记录
class CTRecordModel(models.Model):

	#每条记录唯一标识符
	recordId = models.AutoField(primary_key = True)
	#根据tag区分不同种类的记录，同一个用户相同TAG的事件要严格一致
	recordTag = models.CharField(max_length = 128)
	#userId 外键
	user = models.ForeignKey(CTRUser)
	#recordDate
	recordDate = models.CharField(max_length = 128, default = '0.0')
	#recordDateDayStr
	recordDateDayStr = models.CharField(max_length = 128, default = '0000-00-00')

	def __unicode__(self):
		return self.recordTag + str(self.recordId) +"_"+ str(self.recordDate) + "_" + self.recordDateDayStr

	@staticmethod
	def createAndSaveRecord(user,recordTag,recordDate,recordDateDayStr,points):

		errCode = 0
		errMsg = ""
		if type(recordDate) is not types.StringType and type(recordDate) is not types.UnicodeType:
			errMsg = "recordDate type of"+str(type(recordDate))+" should be string type"
			errCode = -1 
			print "err at creating record:"+errMsg
			return errCode,errMsg
		record = CTRecordModel()
		record.recordTag = recordTag
		record.user = user
		record.recordDate= recordDate
		record.recordDateDayStr = recordDateDayStr

		for point in points:
			if not (point.has_key('key') and point.has_key('timestamp') and point.has_key('index')):
				continue
			key = point['key']
			timestamp = point['timestamp']
			index = point['index']
			if key == None or timestamp == None or index == None:
				continue
			
			record.save()
			tempCode,tempMsg = CTRecordPoint.createAndSavePoint(record,timestamp,key,index)
			if tempCode != 0:
				errCode = tempCode
				errMsg = tempMsg

		if errCode == 0:
			print "record created:" + str(record)
		else:
			print "err at creating record:"+errMsg
		
		return errCode,errMsg

	@staticmethod
	def queryRecordsWithFragment(userId,tag,recordDate,start,end,fragment):

		resultData = []
		records = []
		if not userId or start>end or start<0:
			return records
		if tag and recordDate :
			records = CTRecordModel.objects.filter(user_id = userId).filter(recordTag = tag).filter(recordDateDayStr=recordDate).order_by("-recordDate")[start:end]
		elif tag :
			records = CTRecordModel.objects.filter(user_id = userId).filter(recordTag = tag).order_by("-recordDate")[start:end]
		elif recordDate :
			records = CTRecordModel.objects.filter(user_id = userId).filter(recordDateDayStr=recordDate).order_by("-recordDate")[start:end]
		else :
			records = CTRecordModel.objects.filter(user_id = userId).order_by("-recordDate")[start:end]

		# 时间复杂度O(n)
		tagsArr = []
		#用tag作为key将records放入字典容器	
		recordDicWithTagKey = {}
		for i in range(len(records)):
			recordItem = records[i]
			if not (recordItem.recordTag in tagsArr):
				tagsArr.append(recordItem.recordTag)
				recordDicWithTagKey[recordItem.recordTag] = [recordItem]
			else :
				recordDicWithTagKey[recordItem.recordTag].append(recordItem)
		#将每个tag对应的records按照fragment个切割数组 并生成chart数据
		for i in range(len(tagsArr)):
			tag = tagsArr[i]
			recordsBySpeTag = recordDicWithTagKey[tag]
			tempArr =[]
			for j in range(len(recordsBySpeTag)):
				tempArr.append(recordsBySpeTag[j])
				if len(tempArr)==fragment or j==(len(recordsBySpeTag)-1):
					resultData.append(tempArr)
					tempArr =[]

		return resultData;

#CTRecordPoint
class CTRecordPoint(models.Model):

	#每个点在单条记录内的唯一标识符
	pointId = models.AutoField(primary_key = True)
	#recordId 外键
	fatherRecord = models.ForeignKey(CTRecordModel)
	#记录的原始数据 由于时间精度需达到毫秒以后两位 这里使用char保存从1970到当前的ms数
	timestamp = models.CharField(max_length = 128, default = '0.0')
	#该记录点的键
	key = models.CharField(max_length = 128)
	#该记录点在记录中的次序
	index = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.key + str(self.pointId) + str(self.timestamp)

	@staticmethod
	def createAndSavePoint(fatherRecord,timestamp,key,index):

		errCode = 0
		errMsg = ""
		if type(timestamp) is not types.StringType and type(timestamp) is not types.UnicodeType:
			errMsg = "timestamp type of:" +str(type(timestamp)) +" should be string type"
			errCode = -1 
			return errCode,errMsg
		point = CTRecordPoint()
		point.fatherRecord = fatherRecord
		point.timestamp = timestamp
		point.key = key
		point.index = index
		point.save()
		if errCode == 0:
			print "point created:" + str(point)
		else:
			print "err at creating point:"+errMsg
		return errCode,errMsg

