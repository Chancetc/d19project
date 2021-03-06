from django.http import HttpResponse

import json

class HTTPRSPCode(object):

	OK 					= 		0

	INVALID_PARAMS 		= 		-1
	INVALID_USERNAME 	= 		-2
	INVALID_PWD 		=		-3
	INVALID_FUNCTION	=		-4
	FOBIDDEN_VISIT		=		-5
	OUT_OF_DATE			=		-6
	NOT_LOGIN			=		-7




assert HTTPRSPCode.OK 							== 0
assert HTTPRSPCode.INVALID_PARAMS 				== -1
assert HTTPRSPCode.INVALID_USERNAME 			== -2
assert HTTPRSPCode.INVALID_PWD 					== -3
assert HTTPRSPCode.INVALID_FUNCTION				== -4
assert HTTPRSPCode.FOBIDDEN_VISIT 				== -5
assert HTTPRSPCode.OUT_OF_DATE 					== -6
assert HTTPRSPCode.NOT_LOGIN 					== -7



class ResponseUtil(object):
	"""docstring for ResponseUtil"""
	def __init__(self, arg):
		super(ResponseUtil, self).__init__()
		self.arg = arg

	@staticmethod
	def onResponse(retCode,data,msg):
		return {"msg":msg,"data":data,"retCode":retCode}

	@staticmethod
	def onJsonResponse(retCode,data,msg):
		return HttpResponse(json.dumps(ResponseUtil.onResponse(retCode,data,msg)), content_type = 'application/json')

class RequestUtil(object):
	"""docstring for RequestUtil"""
	def __init__(self, arg):
		super(RequestUtil, self).__init__()
		self.arg = arg
		
	@staticmethod
	def getParamFromRequest(request,key):
		value = ""
		if request.method == 'POST':
			value = request.POST.get(key,'')
		elif request.method == 'GET':
			value = request.GET.get(key,'')
		return value

	@staticmethod
	def getAllParams(request):
		if request.method == 'POST':
			return request.POST
		elif request.method == 'GET':
			return request.GET
		