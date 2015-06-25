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
		print 'user {}'.format(self.current_user)
		self.render("index_expert_bootstrap.html")

	def post(self):
		if self.get_argument('pass', '') != '':
			print 'interview'
			self.redirect("/interview")
			return
		if self.get_argument('logout', '') != '':
			print 'logout'
			# TODO: read host + port from config
			self.redirect(main_front_logout)
			return
		print 'no arg'
		self.redirect("/")

class LogoutHandler(BaseHandler):
	def get(self):
		if not self.get_current_user():
			self.redirect(main_front_auth)
			return
		self.redirect(main_front_logout)


class InterviewHandler(tornado.web.RequestHandler):
	def get(self, page=1):
		# form new interview items
		i_builder = InterviewBuilder()
		i_builder.create_new_interviews()

		db_conn = MongoConnector()
		all_interviews = db_conn.get_all_interviews()
		#print 'got interviews {}'.format(all_interviews)

		pagination = Pagination(all_interviews, int(page), per_page=interview_per_page)
		self.render('interview_list_bootstrap.html',
					pagination=pagination, interview_pass='/interview/pass', endpoint='/interview')

class InterviewItemHandler(tornado.web.RequestHandler):
	def get(self, obj_id):
		db_conn = MongoConnector()
		news_items = db_conn.get_interview_articles(obj_id)
		self.render("interview_item.html", endpoint="/interview/pass/{}".format(obj_id), news_items=news_items)

	def post(self, obj_id, news_cnt):
		news_items = []
		for index in range(int(news_cnt)):
			res = self.get_argument('role_id{}'.format(index), None)
			news_item_id = self.get_argument('obj_id{}'.format(index), None)
			if res is None:
				res = 'bad'
			news_items.append({'id': news_item_id, 'selection': res})
			print 'DEB: Selection for text {}: {}'.format(index, res)

		db_conn = MongoConnector()
		db_conn.update_interview(obj_id, news_items)
		self.write("Thank you for passing through this interview")

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/logout", LogoutHandler),
	(r"/interview", InterviewHandler),
	(r"/interview/(\d+)", InterviewHandler),
	(r"/interview/pass/(?P<obj_id>[\w\d]+)", InterviewItemHandler),
	(r"/interview/pass/(?P<obj_id>[\w\d]+)/(?P<news_cnt>\d+)", InterviewItemHandler),

	(r"/interview/index_files/cloudflare.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/cloudflare.js'}),
	(r"/interview/index_files/ga.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/ga.js'}),
	(r"/interview/index_files/rocket.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/rocket.js'}),
	(r"/interview/index_files/bootstrap-responsive.css()", tornado.web.StaticFileHandler, {'path': '../static/index_files/bootstrap-responsive.css'}),
	(r"/interview/index_files/bootstrap.css()", tornado.web.StaticFileHandler, {'path': '../static/index_files/bootstrap.css'}),
	(r"/interview/index_files/rocket.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/rocket.js'}),

	(r"/css/bootstrap\.css()", tornado.web.StaticFileHandler, {'path': '../static/css/bootstrap.css'}),
	(r"/js/bootstrap.min.js()", tornado.web.StaticFileHandler, {'path': '../static/js/bootstrap.min.js'}),
	(r"/index_files/cloudflare.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/cloudflare.js'}),
	(r"/index_files/ga.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/ga.js'}),
	(r"/index_files/rocket.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/rocket.js'}),
	(r"/index_files/bootstrap-responsive.css()", tornado.web.StaticFileHandler, {'path': '../static/index_files/bootstrap-responsive.css'}),
	(r"/index_files/bootstrap.css()", tornado.web.StaticFileHandler, {'path': '../static/index_files/bootstrap.css'}),
	(r"/index_files/rocket.js()", tornado.web.StaticFileHandler, {'path': '../static/index_files/rocket.js'}),

])

if __name__ == "__main__":
	application.listen(8890)
	tornado.ioloop.IOLoop.instance().start()


