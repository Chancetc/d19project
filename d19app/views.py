#coding:utf-8
from django.shortcuts import render
from d19app.models import CTRUser
from d19app.models import CTRecordModel
from d19app.models import CTRecordPoint
from d19app.HTTPUtil import HTTPRSPCode
from d19app.HTTPUtil import ResponseUtil
from d19app.HTTPUtil import RequestUtil
from d19app.ChartDataUtil import ChartDataUtil
from d19app.DBHelper import DBHelper
from d19app.DateUtil import DateUtil
from d19app.SessionUtil import SessionUtil
from django.http import HttpResponse

import random
import time
import string
import json

# Create your views here.

# Views
def signInByAction(request):
	
	name = RequestUtil.getParamFromRequest(request,'username')
	# users = CTRUser.objects.filter(userName = name)

	# if len(users) == 0:
	# 	print "db without userName:" + name
	# 	return HttpResponse(u"there is no data for user:" + name)
	SessionUtil.setUserNameToSession(request.session,name)
	print "set name:" + name + "to session success"
	return home(request)

def home(request):

	userName = SessionUtil.getUserNameFromSession(request.session)
	if userName == None:
		print "session without userName"
		return login(request)

	#获取当前对象
	print "get name form session:" + userName
	users = CTRUser.objects.filter(userName = userName)
	if len(users) == 0:
		print "db without userName:" + userName
		return login(request)
	return render(request,'home.html')

#用户标签列表
def my_tags(request):
	userId = SessionUtil.getUserIdFromSession(request.session)
	tags = []
	queryRecords = []
	resultRecords = []
	countsDic = {}
	print "my_tags :userId " + str(userId)
	if not userId:
		return login(request)
	else :
		tags,queryRecords,countsDic = queryAllRecorderTags(userId)
	for i in range(len(queryRecords)):
		print queryRecords[i]
		item = {"recordId":queryRecords[i].recordId,"count":countsDic[queryRecords[i].recordTag],"recordTag":queryRecords[i].recordTag,"user_id":queryRecords[i].user_id,"recordDate":float(queryRecords[i].recordDate)/1000.0,"recordDateStr":DateUtil.getDateDayStrFromTimeInterval(float(queryRecords[i].recordDate)/1000.0)}
		resultRecords.append(item)
	data = {'tags':tags,'records':resultRecords}
	return render(request,'record-tags.html',data)

#用户日期列表
def my_dates(request):

	userId = SessionUtil.getUserIdFromSession(request.session)
	dates = []
	tags = []
	queryRecords = []
	resultRecords = []
	print "my_dates :userId " + str(userId)
	if not userId:
		return login(request)
	else :
		dates,records = queryAllRecorderDates(userId)

	data = {'dates':dates,'records':records}
	return render(request,'records-by-date.html',data)

#帮助页面
def user_help(request):

	return render(request,'help.html')
	
#查询结果展示页面
def records_stackedBar(request):

	userId = SessionUtil.getUserIdFromSession(request.session)
	tag = RequestUtil.getParamFromRequest(request,"tag")
	date = RequestUtil.getParamFromRequest(request,"date")
	print "userId " + str(userId)
	if not userId or (not tag and not date):
		print "return home"
		return home(request)

	returnData = {"date":date,"tag":tag}
	return render(request,'stackedBarChart.html',returnData)

#登录页面
def login(request):
	
	if request.session.has_key('userName'):
		del request.session['userName'] 
	if request.session.has_key('userId'):
		del request.session['userId'] 
	return render(request,'login.html')


# interface for request

#上传请求
def uploadRecords(request):

	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = []

	if request.method == 'POST':
		req = json.loads(request.body)
		print req
		if not (req.has_key('userName') and req.has_key('records')):
			retCode = HTTPRSPCode.INVALID_PARAMS
			msg = "userName and records requird"
		else :
			userName = req['userName']
			records = req['records']
			#user = CTRUser.objects.get_or_create(userName=userName)[0]
			retCode,msg = DBHelper.saveRecordsByData(userName,records)
			if len(records) > 0:
				data = records
	else :
		retCode = HTTPRSPCode.INVALID_FUNCTION
		msg = "POST REQUIED"

	return ResponseUtil.onJsonResponse(retCode,data,msg)

#登录请求
def signInByAjaxAction(request):

	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}
	userName = RequestUtil.getParamFromRequest(request,'username')
	password = RequestUtil.getParamFromRequest(request,'password')

	if userName == None:
		msg = "username must not be nil"
		retCode = HTTPRSPCode.INVALID_USERNAME
	else :
		users = CTRUser.objects.filter(userName = userName)
		if len(users) == 0:
			msg = "there is no data for user:" + userName
			retCode = HTTPRSPCode.INVALID_PARAMS
			#success!
		else :
			print request.META
			# print "request.META['HTTP_ORIGIN']:" + str(request.META['HTTP_ORIGIN'])
			homeUrl = str(request.META['HTTP_HOST'])
			if not ("http" in homeUrl or "https" in homeUrl):
				homeUrl = "http://"+homeUrl
			data = {'userName':users[0].userName,'userId':str(users[0].userId),'url':homeUrl}
			SessionUtil.setUserNameToSession(request.session,userName)
			SessionUtil.setUserIdToSession(request.session,users[0].userId)
			print "set name:" + userName + "to session success"
	return ResponseUtil.onJsonResponse(retCode,data,msg)

#查询监控数据请求
def queryRequestForUserRecords(request):
	
	# time.sleep(2)
	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}

	userId = RequestUtil.getParamFromRequest(request,"userId")
	tag = RequestUtil.getParamFromRequest(request,"tag")
	recordDate = RequestUtil.getParamFromRequest(request,"recordDate")
	start = RequestUtil.getParamFromRequest(request,"start")
	end = RequestUtil.getParamFromRequest(request,"end")

	if not userId:
		userId = SessionUtil.getUserIdFromSession(request.session)
	if not userId:
		retCode = HTTPRSPCode.NOT_LOGIN
		msg = "please log in first"
		return ResponseUtil.onJsonResponse(retCode,data,msg)
	if start>end or start<0:
		retCode = HTTPRSPCode.INVALID_PARAMS
		msg = "userId or start&end is valid"
		return ResponseUtil.onJsonResponse(retCode,data,msg)
	#data from db
	dbRecords = CTRecordModel.queryRecordsWithFragment(userId,tag,recordDate,start,end,10)
	recordData = []
	for i in range(len(dbRecords)):
		chartDateItem = ChartDataUtil.getChartDataFromDBRecordsArr(dbRecords[i])
	 	recordData.append(chartDateItem)

	data["records"] = recordData;
	data["count"] = len(recordData)
	return ResponseUtil.onJsonResponse(retCode,data,msg)

#查询所有标签请求
def queryRequetForAllRecorderTags(request):

	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}
	userId = SessionUtil.getUserIdFromSession(request.session)
	tags = []
	queryRecords = []
	resultRecords = []
	print "userId " + str(userId)
	if not userId:
		retCode = HTTPRSPCode.NOT_LOGIN
		msg = "user not login"
	else :
		tags,queryRecords,counts = queryAllRecorderTags(userId)
	for i in range(len(queryRecords)):
		print queryRecords[i]
		item = {"recordId":queryRecords[i].recordId,"recordTag":queryRecords[i].recordTag,"user_id":queryRecords[i].user_id,"recordDate":queryRecords[i].recordDate,"recordDateStr":DateUtil.getDateDayStrFromTimeInterval(float(queryRecords[i].recordDate)/1000.0)}
		resultRecords.append(item)
	data = {'tags':tags,'records':resultRecords}
	return ResponseUtil.onJsonResponse(retCode,data,msg)


def queryAllRecorderTags(userId):

	tags = CTRecordModel.objects.filter(user_id = userId).values('recordTag').distinct()
	tagArr = []
	records = []
	counts = {}
	for i in range(len(tags)):
		recorder = CTRecordModel.objects.filter(user_id = userId).filter(recordTag=tags[i]["recordTag"]).order_by("-recordDate")
		counts[tags[i]["recordTag"]] = len(recorder)
		records.append(recorder[0])
		tagArr.append(tags[i]["recordTag"])
	records.sort(recordModelComp)
	return tagArr,records,counts

#查询所有日期请求
def queryAllRecorderDates(userId):
	dates = CTRecordModel.objects.filter(user_id=userId).values('recordDateDayStr').distinct()
	records = []
	counts =[]
	for i in range(len(dates)):
		items = CTRecordModel.objects.filter(user_id=userId).filter(recordDateDayStr=dates[i]["recordDateDayStr"])
		itemTags = CTRecordModel.objects.filter(user_id=userId).filter(recordDateDayStr=dates[i]["recordDateDayStr"]).values('recordTag').distinct()

		itemTagsValues = []
		for j in range(len(itemTags)):
			itemTagsValues.append(itemTags[j]["recordTag"])
		records.append({"date":dates[i]["recordDateDayStr"],"tags":itemTagsValues,"count":len(items)})
	records.sort(dateStrComp)
	return dates,records

#util -------------------------------

def recordModelComp(a,b):

	date1 = float(a.recordDate)
	date2 = float(b.recordDate)
	if date1 < date2:
		return 1
	elif date1 > date2:
		return -1
	else :
		return 0

def dateStrComp(a,b):
	
	print a
	date1 = a["date"]
	date2 = b["date"]
	if date1 < date2:
		return 1
	elif date1 > date2:
		return -1
	else :
		return 0
