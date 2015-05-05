#!/usr/bin/python
import urllib3
import json

class Connector:
		def __send_req__(self, method, url, headers=None, fields=None):
				headers = headers or {}
				fields = fields or {}
				http = urllib3.PoolManager()

				try:
						if method == 'GET':
								resp = http.request(method, url, headers=headers, fields=fields)
						# TODO: add other methods
						else:
								resp = None

						if resp is None:
							print('ERR: empty response')
							return None

						if resp.status != 200:
							print('INF: bad response (status {})'.format(res.status))
							return None

						return resp
				except Exception as ex:
						print('ERR: {}'.format(ex))
						return None

		def get(self, url, headers=None):
				resp = self.__send_req__('GET', url, headers)
				return resp



