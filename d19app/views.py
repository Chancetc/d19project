#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from d19app.models import CTRUser
from d19app.models import CTRecordModel
from d19app.models import CTRecordPoint

import random
import json
import time

# Create your views here.
def my_login(request):

	#db save
	user = CTRUser()
	user.userName = "test"
	user.password = "123456"
	user.save()

	record = CTRecordModel()
	record.recordTag = "comic"
	record.user = user
	record.save()

	point = CTRecordPoint()
	point.fatherRecord = record
	point.key = "operation"
	point.timestamp = str(time.time())
	point.index = 0
	point.save()

	#db get
	users = CTRUser.objects.all().order_by("-userId")[:10]

	records = CTRecordModel.objects.all().order_by("-recordDate")[:10]

	points = CTRecordPoint.objects.all().order_by("-timestamp")[:10]
	
	name_dict = {'user': users[0].userName+str(users[0].userId), 'record': records[0].recordTag+str(records[0].recordId),'operation':points[0].key+str(points[0].pointId)}
	return HttpResponse(json.dumps(name_dict), content_type='application/json')

def index(request):
	return HttpResponse(u"Hello World! This is CTRecorder!")

def home(request):

	return render(request,'home.html')

def highChartDemo(request):
	chartData = u"\"[{name:'-[QQExtendTableViewControllerProvider tableView:didSelectRowAtIndexPath:]~-[QQForwardEngine ActionOpenComicCenter:]',data:[1.98,0.43,14.48,0.33,0.43,0.65,0.34,1.88,7.41,2.73]},{name:'-[QQForwardEngine ActionOpenComicCenter:]~-[QQVIPFunctionComicPortalViewController init]',data:[0.97,0.23,0.25,0.18,0.26,0.36,0.18,0.38,0.38,0.26]},{name:'-[QQVIPFunctionComicPortalViewController init]~-[QQVIPFunctionComicPortalViewController loadView]',data:[1.15,0.86,1,0.77,0.92,5.35,0.7,1.51,1.18,0.95]},{name:'-[QQVIPFunctionComicPortalViewController loadView]~-[QQVIPFunctionComicPortalViewController viewDidLoad]',data:[0.16,0.16,0.2,0.12,0.2,0.18,0.19,0.19,0.21,0.19]},{name:'-[QQVIPFunctionComicPortalViewController viewDidLoad]~QQVIPFunctionComicPortalViewController_homeVCinit',data:[0.15,0.09,0.18,0.13,0.17,0.12,0.11,0.11,0.17,0.16]},{name:'QQVIPFunctionComicPortalViewController_homeVCinit~QQVIPFunctionComicPortalViewController_loadcomicsEnd',data:[20.27,17.51,8.69,38.66,16.94,16.16,16.52,31.7,17.12,17]},{name:'QQVIPFunctionComicPortalViewController_loadcomicsEnd~-[QQVIPFunctionComicPortalViewController viewWillAppear:]',data:[4.84,3.11,24.2,3.05,2.75,3.02,2.68,5.48,2.97,2.64]},{name:'-[QQVIPFunctionComicPortalViewController viewWillAppear:]~-[QQVIPFunctionComicWebViewController loadRequest:]',data:[103.49,86.14,74.69,56.74,88.79000000000001,93.68000000000001,103.91,69.54000000000001,61.93,56.3]},{name:'-[QQVIPFunctionComicWebViewController loadRequest:]~QQVIPFunctionComicPortalViewController_bkbegine',data:[151.22,118.74,104.61,43.27,112.18,58.8,136.73,56.15,115.77,110.46]},{name:'QQVIPFunctionComicPortalViewController_bkbegine~QQVIPFunctionComicPortalViewController_webviews',data:[141.16,131.18,153.13,194.25,106.84,206.26,177.9,123.39,47.16,102.03]},{name:'QQVIPFunctionComicPortalViewController_webviews~QQVIPFunctionComicPortalViewController_adds views',data:[3.42,3.05,3.39,3.41,2.81,3.89,3.46,4.09,3.94,3.34]},{name:'QQVIPFunctionComicPortalViewController_adds views~achive',data:[599.48,469.22,607.78,419.43,441.32,431.03,484.54,481.59,391.95,352.76]}]\""
	return render(request,'stackedBarChartTest.html',{'chartData':chartData})

def uploadRecords(request):
	valueList = request.POST['records']
	return HttpResponse(valueList, content_type = 'application/json')


