#!/usr/bin/python
import urllib3
import json

class Connector:
		def send_req(self, method, url, headers=None, fields=None):
				headers = headers or {}
				fields = fields or {}
				http = urllib3.PoolManager()

				try:
						if method == 'PUT':
							resp = http.urlopen(method, header=headers, body=json.dumps(fields))
						else:
							resp = http.request(method, url, headers=headers, fields=fields)

						if resp is None:
							print('ERR: empty response')
							return None

						print("INF: recv status={}".format(resp.status)

						return resp
				except Exception as ex:
						print('ERR: {}'.format(ex))
						return None

