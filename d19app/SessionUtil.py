class SessionUtil(object):
	"""docstring for SessionUtil"""
	def __init__(self, arg):
		super(SessionUtil, self).__init__()
		self.arg = arg

	@staticmethod
	def getUserNameFromSession(session):

		name = ""
		if session.has_key('userName'):
			name = session['userName']
		return name

	@staticmethod
	def setUserNameToSession(session,username):

		session['userName'] = username
		pass

	@staticmethod
	def setUserIdToSession(session,userId):

		session['userId'] = userId
		pass
	@staticmethod
	def getUserIdFromSession(session):
		userId = ""
		if session.has_key('userId'):
			userId = session['userId']
		return userId
		