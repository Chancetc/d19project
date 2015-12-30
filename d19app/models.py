#coding:utf-8
from django.db import models
from datetime import datetime
from django.utils import timezone
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
		return self.userName
		

#CTRModel表:单条记录
class CTRecordModel(models.Model):

	#每条记录唯一标识符
	recordId = models.AutoField(primary_key = True)
	#根据tag区分不同种类的记录，同一个用户相同TAG的事件要严格一致
	recordTag = models.CharField(max_length = 128)
	#userId 外键
	userId = models.ForeignKey(CTRUser)

	def __unicode__(self):
		return self.recordTag + str(self.recordId)


#CTRecordPoint
class CTRecordPoint(models.Model):

	#每个点在单条记录内的唯一标识符
	pointId = models.AutoField(primary_key = True)
	#recordId 外键
	recordId = models.ForeignKey(CTRecordModel)
	#记录的原始数据
	recordDate = models.DateTimeField();
	#该记录点的键
	key = models.CharField(max_length = 128)
	#该记录点在记录中的次序
	index = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.key + str(self.pointId)


