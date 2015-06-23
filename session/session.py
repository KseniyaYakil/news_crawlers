#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import tornado.httputil as util
import json
from mysql_connector import MySQLConnector

class AuthUserHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(200)
		user_cookie = self.get_argument('user_cookie', '')
		if not user_cookie:
			self.set_status(400, reason='incorrect data')
			print 'INF: incorrect request data'
			return
		print 'INF: check cookie {} in db'.format(user_cookie)
		user_cn = MySQLConnector()
		user_id = user_cn.get_user_by_cookie(user_cookie)
		if user_id is None:
			self.set_status(401, reason='no user for cookie')
			return

	def put(self):
		user_data = json.loads(self.request.body)

		print "DEB: add user {}".format(user_data['username'])
		user_cn = MySQLConnector()
		user_id = user_cn.insert_user(user_data)

		if user_id  != None:
			self.set_status(201)
		else:
			self.set_status(409, reason='unable to insert user')

	def post(self):
		self.set_status(202)
		user_data = {'username': '', 'password': ''}
		files = {}
		headers = {}
		util.parse_body_arguments(self.request.headers['Content-Type'], self.request.body, files, headers)

		for k in user_data.keys():
			if k not in files.keys():
				self.set_status(400, reason='incorrect data')
				print 'INF: incorrect request data'
				return
			user_data[k] = files[k][0]

		print "DEB: login username " + user_data['username']
		user_cn = MySQLConnector()
		user_cookie = user_cn.create_cookie(user_data)
		if user_cookie is None:
			self.set_status(401, reason='no such user-password pair') # unauthorized
			return

		self.write(json.dumps({'user_cookie': user_cookie}))

	def delete(self):
		self.set_status(200)
		user_cookie = self.get_argument('user_cookie', '')
		if not user_cookie:
			self.set_status(400, reason='incorrect data')
			print 'INF: incorrect request data'
			return

		user_cn = MySQLConnector()
		user_cn.del_cookie(user_cookie)
		print 'INF: cookie {} was deleted'.format(user_cookie)

class RoleHandler(tornado.web.RequestHandler):
	def get(self):
		user_cookie = self.get_argument('user_cookie', '')
		if not user_cookie:
			self.set_status(400, reason='incorrect data')
			print 'INF: incorrect request data'
			return
		user_cn = MySQLConnector()
		role_id = user_cn.role_by_cookie(user_cookie)

		self.write(json.dumps({'id': role_id}))

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(json.dumps({'ok': 'ok'}))

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/auth", AuthUserHandler),
	(r"/role", RoleHandler),
])

if __name__ == "__main__":
	application.listen(8887)
	tornado.ioloop.IOLoop.instance().start()

