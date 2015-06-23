#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import sys
sys.path.append("../util")
from session_agent import SessionAgent
from base_handler import BaseHandler

main_front = 'http://127.0.0.1:8888'
main_front_auth = main_front + '/auth'
main_front_logout = main_front + '/logout'

class MainHandler(BaseHandler):
	def get(self):
		if not self.get_current_user():
			self.redirect(main_front_auth)
			return
		self.render("index_researcher.html")

	def post(self):
		user_cookie = self.get_current_user()
		if not user_cookie:
			self.redirect(main_front_auth)
			return

		if self.get_argument('show', '') != '':
			self.redirect("/results")
			return
		if self.get_argument('logout', '') != '':
			self.redirect(main_front_logout)
			return
		self.redirect("/")

class ResultsHandler(BaseHandler):
	def get(self):
		self.write("results here")

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/results", ResultsHandler)
])

if __name__ == "__main__":
	application.listen(8891)
	tornado.ioloop.IOLoop.instance().start()


