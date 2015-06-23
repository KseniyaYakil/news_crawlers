import urllib3
import json

class Connector:
	def send_req(self, url, method, headers=None, fields=None):
		headers = headers or {}
		fields = fields or {}
		http = urllib3.PoolManager()

		try:
			print 'DEB: send {} req to {}'.format(method, url)
			if method == 'PUT':
				resp = http.urlopen(method, url, headers=headers, body=json.dumps(fields))
			else:
				resp = http.request(method, url, headers=headers, fields=fields)

			if resp is None:
				print 'ERR: empty response'
				return None

			print "INF: recv status={}".format(resp.status)
			return resp
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

class SessionAgent:
	def __init__(self):
		#session host and port
		self.host = '127.0.0.1'
		self.port = '8887'
		self.url = 'http://' + self.host + ':' + self.port
		self.auth_user = '/auth'
		self.role_user = '/role'
		self.conn = Connector()

	def register_user(self, user_data):
		return self.conn.send_req(url=self.url + self.auth_user, method='PUT', fields=user_data)

	def self_login_user(self, user_data):
		return self.conn.send_req(url=self.url + self.auth_user, method='POST', fields=user_data)

	def self_logout_user(self, user_data):
		return self.conn.send_req(url=self.url + self.auth_user, method='DELETE', fields=user_data)

	def is_authorized(self, user_data):
		return self.conn.send_req(url=self.url + self.auth_user, method='GET', fields=user_data)

	def get_role_by_cookie(self, user_data):
		return self.conn.send_req(url=self.url + self.role_user, method='GET', fields=user_data)

