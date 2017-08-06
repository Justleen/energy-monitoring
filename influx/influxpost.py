import ssl
from httplib import HTTPSConnection

class post(object):
	def __init__(self):
		self.host 		= 'monitoring.aardehuis.nl'
		self.port 		= 8086
		self.wachtwoord 	= 'Sk1nnyp1nkelephant'
		self.username	= 'leen'
		self.dbname 		= 'db_name'
		self.context = ssl._create_unverified_context()
		self.headers = {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain'}

	
	def httpsPost(self, body):
		conn = HTTPSConnection(self.host,self.port,context=self.context)
		conn.set_debuglevel(7)
		conn.request('POST', '/write?db={db}&u={user}&p={password}'.format(db=self.dbname, user=self.username, password=self.wachtwoord), body, self.headers) 
		conn.close()
