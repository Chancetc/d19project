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
	userName = models.CharField(max_length = 32)
	password = models.CharField(max_length = 128, blank = True, null = True)
	Email = models.EmailField(blank = True, null = True)
	registerDate = models.DateTimeField(auto_now_add = True) 
	lastLoginDate = models.DateTimeField(default = timezone.now, blank = True, null = True)

	def __unicode__(self):
		return self.userName
		