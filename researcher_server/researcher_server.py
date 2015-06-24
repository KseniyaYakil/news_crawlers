#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import sys
sys.path.append("../util")
from session_agent import SessionAgent
from base_handler import BaseHandler
from paginator import Pagination
from mongodb_connector import MongoConnector

main_front = 'http://127.0.0.1:8888'
main_front_auth = main_front + '/auth'
main_front_logout = main_front + '/logout'
interview_per_page = 2

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
	def get(self, page=1):
		db_conn = MongoConnector()
		all_interviews = db_conn.get_all_interviews()

		pagination = Pagination(all_interviews, int(page), per_page=interview_per_page)
		self.render('results_list.html',
					pagination=pagination, results_show='/results/show', endpoint='/results')

class ResultsItemHandler(BaseHandler):
	def get(self, obj_id):
		db_conn = MongoConnector()
		interview_item = db_conn.get_interview(obj_id)
		self.render("results_item.html", interview_info=interview_item)

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/results", ResultsHandler),
	(r"/results/(\d+)", ResultsHandler),
	(r"/results/show/(?P<obj_id>[\d\w]+)", ResultsItemHandler),
])

if __name__ == "__main__":
	application.listen(8891)
	tornado.ioloop.IOLoop.instance().start()
