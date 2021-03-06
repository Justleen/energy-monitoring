import ssl
from httplib import HTTPSConnection
import logging

import ConfigParser
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
import socket

socket.setdefaulttimeout(1)


#config
Config = ConfigParser.ConfigParser()
Config.readfp(open( dir_path.replace('influx','') + '/config.ini'))
Config.read('../config.ini')

#logging
log = logging.getLogger(__name__)



log = logging.getLogger(__name__)

class post(object):
	def __init__(self):
		self.host 			= Config.get('influxdb', 'influxHost')
		self.port 			= Config.get('influxdb', 'port')
		self.wachtwoord 	= Config.get('influxdb', 'wachtwoord')
		self.username		= Config.get('influxdb', 'username')
		self.dbname 		= Config.get('influxdb', 'dbname')
		self.context 		= ssl._create_unverified_context()
		self.headers 		= {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain'}

	def httpsPost(self, body):
		try:
			conn = HTTPSConnection(self.host,self.port,context=self.context)
			#conn.set_debuglevel(1)
			conn.request('POST', '/write?db={db}&u={user}&p={password}'.format(db=self.dbname, user=self.username, password=self.wachtwoord), body, self.headers) 
			response = conn.getresponse()
			log.debug(body)
			log.info('Updated Influx. HTTP response {}'.format(response.status))
		except socket.error as e:
			print(e)
			log.error("oops socket errors! I'll pass")
			pass
		#except Exception as e:
		#	raise influxPostError(e)
		#	log.info("couldn't post to https: %s", e )
		conn.close()     

class influxPostError(Exception):
	pass
