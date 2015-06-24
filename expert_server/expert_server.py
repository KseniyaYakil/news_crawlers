#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import sys
sys.path.append("../util")
from session_agent import SessionAgent
from base_handler import BaseHandler
from paginator import Pagination

from mongodb_connector import MongoConnector
from interview_builder import InterviewBuilder

main_front = 'http://127.0.0.1:8888'
main_front_auth = main_front + '/auth'
main_front_logout = main_front + '/logout'
interview_per_page = 2

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
	def get(self, page=1):
		# form new interview items
		i_builder = InterviewBuilder()
		i_builder.create_new_interviews()

		db_conn = MongoConnector()
		all_interviews = db_conn.get_all_interviews()
		print 'got interviews {}'.format(all_interviews)

		pagination = Pagination(all_interviews, int(page), per_page=interview_per_page)
		self.render('interview_list.html',
					pagination=pagination, interview_pass='pass', endpoint='/interview')

class InterviewItemHandler(tornado.web.RequestHandler):
	def get(self, obj_id):
		self.write("Interview item {}".format(obj_id))

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/interview", InterviewHandler),
	(r"/interview/(\d+)", InterviewHandler),
	(r"/interview/pass/(?P<obj_id>[\w\d]+)", InterviewItemHandler),
])

if __name__ == "__main__":
	application.listen(8890)
	tornado.ioloop.IOLoop.instance().start()


