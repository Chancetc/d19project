#coding:utf-8
from django.shortcuts import render
from d19app.models import CTRUser
from d19app.models import CTRecordModel
from d19app.models import CTRecordPoint
from d19app.HTTPUtil import HTTPRSPCode
from d19app.HTTPUtil import ResponseUtil
from django.http import HttpResponse

import random
import time
import string
import json

# Create your views here.
def my_login(request):

	#db get

	users = CTRUser.objects.all().order_by("-userId")[:10]

	records = CTRecordModel.objects.all().order_by("-recordDate")[:10]

	points = CTRecordPoint.objects.all().order_by("-timestamp")[:10]
	
	req = "nothing"
	if request.method == 'POST':
		req = request.body
	
	return home(request)
	name_dict = {'req':req,'user': users[0].userName+str(users[0].userId), 'record': records[0].recordTag+str(records[0].recordId)+str(records[0].recordDate),'operation':points[0].key+str(points[0].pointId)+str(points[0].timestamp)}
	return HttpResponse(json.dumps(name_dict), content_type='application/json')

def signInByAjaxAction(request):

	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}
	userName = getPostParamFromRequest(request,'username')
	password = getPostParamFromRequest(request,'password')

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
			setUserNameToSession(request.session,userName)
			setUserIdToSession(request.session,users[0].userId)
			print "set name:" + userName + "to session success"
	return ResponseUtil.onJsonResponse(retCode,data,msg)

def signInByAction(request):
	
	name = getPostParamFromRequest(request,'username')
	# users = CTRUser.objects.filter(userName = name)

	# if len(users) == 0:
	# 	print "db without userName:" + name
	# 	return HttpResponse(u"there is no data for user:" + name)

	setUserNameToSession(request.session,name)
	print "set name:" + name + "to session success"
	return home(request)

def home(request):

	userName = getUserNameFromSession(request.session)

	if userName == None:
		print "session without userName"
		return login(request)

	#获取当前对象
	print "get name form session:" + userName
	#TODO: 查询不到会崩溃

	users = CTRUser.objects.filter(userName = userName)

	if len(users) == 0:
		print "db without userName:" + userName
		return login(request)
	return render(request,'home.html',{'chartData':[],'firstDate':"",'dateList':[],'tag':""})

def my_tags(request):
	userId = getUserIdFromSession(request.session)
	tags = []
	queryRecords = []
	resultRecords = []
	print "my_tags :userId " + str(userId)
	if not userId:
		return login(request)
	else :
		tags,queryRecords = queryAllRecorderTags(userId)
	for i in range(len(queryRecords)):
		print queryRecords[i]
		item = {"recordId":queryRecords[i].recordId,"recordTag":queryRecords[i].recordTag,"user_id":queryRecords[i].user_id,"recordDate":float(queryRecords[i].recordDate)/1000.0,"recordDateStr":getDateDayStrFromTimeInterval(float(queryRecords[i].recordDate)/1000.0)}
		resultRecords.append(item)
	data = {'tags':tags,'records':resultRecords}
	return render(request,'record-tags.html',data)

def user_help(request):

	return render(request,'help.html')
	
def records_stackedBar(request):

	userId = getUserIdFromSession(request.session)
	tag = request.GET.get("tag",'')
	print "userId " + str(userId)
	if not userId or not tag:
		return home(request)

	#取出当前对象对应的最近10条记录 按记录时间排序

	records = CTRecordModel.objects.filter(user_id = userId).filter(recordTag = tag).order_by("-recordDate")[:100]
	print records

	if records == None or len(records) == 0:
		return HttpResponse(u'do not have any record!');

	chartData,firstDate,dateList,tag= getHighChartDataFromRecords(records)

	print "\nchartData:" + chartData + "\nfirstDate:" + firstDate + "\ndateList:" + str(dateList) + "\ntag:" + tag
	
	#chartData = u"\"[{name:'-[QQExtendTableViewControllerProvider tableView:didSelectRowAtIndexPath:]~-[QQForwardEngine ActionOpenComicCenter:]',data:[1.98,0.43,14.48,0.33,0.43,0.65,0.34,1.88,7.41,2.73]},{name:'-[QQForwardEngine ActionOpenComicCenter:]~-[QQVIPFunctionComicPortalViewController init]',data:[0.97,0.23,0.25,0.18,0.26,0.36,0.18,0.38,0.38,0.26]},{name:'-[QQVIPFunctionComicPortalViewController init]~-[QQVIPFunctionComicPortalViewController loadView]',data:[1.15,0.86,1,0.77,0.92,5.35,0.7,1.51,1.18,0.95]},{name:'-[QQVIPFunctionComicPortalViewController loadView]~-[QQVIPFunctionComicPortalViewController viewDidLoad]',data:[0.16,0.16,0.2,0.12,0.2,0.18,0.19,0.19,0.21,0.19]},{name:'-[QQVIPFunctionComicPortalViewController viewDidLoad]~QQVIPFunctionComicPortalViewController_homeVCinit',data:[0.15,0.09,0.18,0.13,0.17,0.12,0.11,0.11,0.17,0.16]},{name:'QQVIPFunctionComicPortalViewController_homeVCinit~QQVIPFunctionComicPortalViewController_loadcomicsEnd',data:[20.27,17.51,8.69,38.66,16.94,16.16,16.52,31.7,17.12,17]},{name:'QQVIPFunctionComicPortalViewController_loadcomicsEnd~-[QQVIPFunctionComicPortalViewController viewWillAppear:]',data:[4.84,3.11,24.2,3.05,2.75,3.02,2.68,5.48,2.97,2.64]},{name:'-[QQVIPFunctionComicPortalViewController viewWillAppear:]~-[QQVIPFunctionComicWebViewController loadRequest:]',data:[103.49,86.14,74.69,56.74,88.79000000000001,93.68000000000001,103.91,69.54000000000001,61.93,56.3]},{name:'-[QQVIPFunctionComicWebViewController loadRequest:]~QQVIPFunctionComicPortalViewController_bkbegine',data:[151.22,118.74,104.61,43.27,112.18,58.8,136.73,56.15,115.77,110.46]},{name:'QQVIPFunctionComicPortalViewController_bkbegine~QQVIPFunctionComicPortalViewController_webviews',data:[141.16,131.18,153.13,194.25,106.84,206.26,177.9,123.39,47.16,102.03]},{name:'QQVIPFunctionComicPortalViewController_webviews~QQVIPFunctionComicPortalViewController_adds views',data:[3.42,3.05,3.39,3.41,2.81,3.89,3.46,4.09,3.94,3.34]},{name:'QQVIPFunctionComicPortalViewController_adds views~achive',data:[599.48,469.22,607.78,419.43,441.32,431.03,484.54,481.59,391.95,352.76]}]\""
	return render(request,'stackedBarChart.html',{'chartData':chartData,'firstDate':firstDate,'dateList':dateList,'tag':tag})

def login(request):
	
	if request.session.has_key('userName'):
		del request.session['userName'] 
	if request.session.has_key('userId'):
		del request.session['userId'] 
	return render(request,'login.html')

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
			retCode,msg = saveRecordsByData(userName,records)
			if len(records) > 0:
				data = records
	else :
		retCode = HTTPRSPCode.INVALID_FUNCTION
		msg = "POST REQUIED"

	return ResponseUtil.onJsonResponse(retCode,data,msg)


#util -------------------------------


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
			recordDateDayStr = getDateDayStrFromTimeInterval(float(recordDate)/1000.0)
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

def saveSetValue(obj, key, value):

	if obj != None and key != None and value != None:
		obj[key] = value
	return obj

def saveGetValue(obj,key):

	if obj != None and key != None and obj.has_key(key):
		return obj[key]
	pass

def getUserNameFromSession(session):

	name = ""
	if session.has_key('userName'):
		name = session['userName']
	return name

def setUserNameToSession(session,username):

	session['userName'] = username
	pass
def setUserIdToSession(session,userId):
	session['userId'] = userId
	pass

def getUserIdFromSession(session):
	userId = ""
	if session.has_key('userId'):
		userId = session['userId']
	return userId

def getPostParamFromRequest(request,key):
	
	value = ""
	if request.method == 'POST':
		value = request.POST.get(key,'')
	return value

def getHighChartDataFromRecords(records):
	#取出每条记录对应的所有记录点 按序号排序

	print "length of oringinal"
	print len(records)

	timesArr = []
	standardKeys = ''
	standardKeyArr = []
	dateList = []

	for record in records:

		points = CTRecordPoint.objects.filter(fatherRecord = record).order_by("index")

		if points == None or len(points) == 0 :
			continue 

		lastKey = ''
		lastTime = 0

		keys = []
		times = []
		print "\n##############################"
		print points
		print "##############################"
		#创建 key数组和时间数组
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

		#去掉不合群的记录
		print "standardKeys: " + standardKeys + "\ncurrentKeys: " + thisKeys
		if thisKeys == standardKeys:
			times.reverse()
			timesArr.append(times)
			dateList.append(getDateStrFromTimeInterval(float(record.recordDate)/1000.0))
		else :
			print "this key IS not equal to standard key!"

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

	#for循环数组 重组
	#[{name: 'John',data: [5, 3, 4, 7, 2]},{name: 'Jane',data: [2, 2, 3, 2, 1]},{name: 'Joe',data: [3, 4, 4, 2, 5]}]

	print "\nresult of getHighChartDataFromRecords:" + resultStr

	print "length of result :"
	print len(dateList)
	return resultStr,getDateDayStrFromTimeInterval(float(records[0].recordDate)/1000.0),dateList,records[0].recordTag

def getDateStrFromTimeInterval(timeInterval):

	timeArray = time.localtime(timeInterval)
	dateStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	dateStr = dateStr + " ("+ str(timeInterval) + ")"
	return dateStr

def getDateDayStrFromTimeInterval(timeInterval):

	timeArray = time.localtime(timeInterval)
	dateStr = time.strftime("%Y-%m-%d", timeArray)
	return dateStr

# interface for ajax request

def queryRecords(userId,tag,recordDate,start,end):

	resultData = []
	records = []
	if not userId or start>end or start<0:
		return records
	if tag and recordDate :
		records = CTRecordModel.objects.filter(user_id = userId).filter(recordTag = tag).filter(recordDateDayStr=recordDate).order_by("-recordDate")[start:end]
	elif tag :
		records = CTRecordModel.objects.filter(user_id = userId).filter(recordTag = tag).order_by("-recordDate")[start:end]
	else :
		records = CTRecordModel.objects.filter(user_id = userId).order_by("-recordDate")[start:end]
		# 如何分类
	# 时间复杂度O(n)
	tagsArr = []
	recordDicWithTagKey = {}
	for i in range(len(records)):
		recordItem = records[i]
		if not (recordItem.recordTag in tagsArr):
			tagsArr.append(recordItem.recordTag)
			recordDicWithTagKey[recordItem.recordTag] = [recordItem]
		else :
			recordDicWithTagKey[recordItem.recordTag].append(recordItem)
	print "length"
	print recordDicWithTagKey
	for i in range(len(tagsArr)):
		tag = tagsArr[i]
		recordsBySpeTag = recordDicWithTagKey[tag]
		tempArr =[]
		for j in range(len(recordsBySpeTag)):
			tempArr.append(recordsBySpeTag[j])
			if len(tempArr)==10 or j==(len(recordsBySpeTag)-1):
				chartData,firstDate,dateList,tag= getHighChartDataFromRecords(tempArr)
				dataItem = {'chartData':chartData,'firstDate':firstDate,'dateList':dateList,'tag':tag}
				resultData.append(dataItem)
				tempArr =[]

	return resultData;

def queryRequestForUserRecords(request):
	
	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}

	userId = getPostParamFromRequest(request,"userId")
	tag = getPostParamFromRequest(request,"tag")
	recordDate = getPostParamFromRequest(request,"recordDate")
	start = getPostParamFromRequest(request,"start")
	end = getPostParamFromRequest(request,"end")

	if not userId:
		userId = getUserIdFromSession(request.session)
	if not userId:
		retCode = HTTPRSPCode.NOT_LOGIN
		msg = "please log in first"
		return ResponseUtil.onJsonResponse(retCode,data,msg)
	if start>end or start<0:
		retCode = HTTPRSPCode.INVALID_PARAMS
		msg = "userId or start&end is valid"
		return ResponseUtil.onJsonResponse(retCode,data,msg)
	records = queryRecords(userId,tag,recordDate,start,end)
	data["records"] = records;
	data["count"] = len(records)
	return ResponseUtil.onJsonResponse(retCode,data,msg)

def queryRequetForAllRecorderTags(request):

	retCode = HTTPRSPCode.OK
	msg = "ok"
	data = {}
	userId = getUserIdFromSession(request.session)
	tags = []
	queryRecords = []
	resultRecords = []
	print "userId " + str(userId)
	if not userId:
		retCode = HTTPRSPCode.NOT_LOGIN
		msg = "user not login"
	else :
		tags,queryRecords = queryAllRecorderTags(userId)
	for i in range(len(queryRecords)):
		print queryRecords[i]
		item = {"recordId":queryRecords[i].recordId,"recordTag":queryRecords[i].recordTag,"user_id":queryRecords[i].user_id,"recordDate":queryRecords[i].recordDate,"recordDateStr":getDateDayStrFromTimeInterval(float(queryRecords[i].recordDate)/1000.0)}
		resultRecords.append(item)
	data = {'tags':tags,'records':resultRecords}
	return ResponseUtil.onJsonResponse(retCode,data,msg)


def queryAllRecorderTags(userId):

	tags = CTRecordModel.objects.filter(user_id = userId).values('recordTag').distinct()
	tagArr = []
	records = []
	for i in range(len(tags)):
		recorder = CTRecordModel.objects.filter(user_id = userId).filter(recordTag=tags[i]["recordTag"]).order_by("-recordDate")[:1]
		records.append(recorder[0])
		tagArr.append(tags[i]["recordTag"])
	records.sort(recordModelComp)
	return tagArr,records
	
def recordModelComp(a,b):

	date1 = float(a.recordDate)
	date2 = float(b.recordDate)
	if date1 < date2:
		return 1
	elif date1 > date2:
		return -1
	else :
		return 0
