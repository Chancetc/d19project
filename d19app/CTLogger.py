import logging  
import logging.handlers

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

class CTLogger(object):
	"""docstring for CTLogger"""
	def __init__(self, x=0):
		self.x = x
		logging.basicConfig(level=logging.DEBUG,
						format='\n%(levelname)s %(asctime)s %(filename)s %(funcName)s[line:%(lineno)d] \n%(message)s',
						datefmt='%a, %d %b %Y %H:%M:%S',
						filename='ctrecorder.log',
						filemode='w')

		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)
		formatter = logging.Formatter('\n%(levelname)s %(asctime)s %(filename)s %(funcName)s[line:%(lineno)d] \n%(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

@singleton    
class LoggerInstance(object):    
    logger =  CTLogger()  
    def __init__(self, x=0):    
        self.x = x   
		