#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import sys
sys.path.append("../util")
from session_agent import SessionAgent
from base_handler import BaseHandler
from mongodb_connector import MongoConnector
from interview_builder import InterviewBuilder

main_front = 'http://127.0.0.1:8888'
main_front_auth = main_front + '/auth'
main_front_logout = main_front + '/logout'

class MainHandler(BaseHandler):
	def get(self):
		if not self.get_current_user():
			self.redirect(main_front_auth)
			return
		self.render("index_expert.html")

	def post(self):
		user_cookie = self.get_current_user()
		if not user_cookie:
			self.redirect(main_front_auth)
			return

		if self.get_argument('pass', '') != '':
			self.redirect("/interview")
			return
		if self.get_argument('logout', '') != '':
			# TODO: read host + port from config
			self.redirect(main_front_logout)
			return
		self.redirect("/")

class InterviewHandler(tornado.web.RequestHandler):
	def get(self):
		# form new interview items
		i_builder = InterviewBuilder()
		i_builder.create_new_interviews()

		# select list of interviews - paging?
		self.write("Interview")

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/interview", InterviewHandler)
])

if __name__ == "__main__":
	application.listen(8890)
	tornado.ioloop.IOLoop.instance().start()


