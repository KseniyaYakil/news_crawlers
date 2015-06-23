#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web
import json
import sys
sys.path.append("../util")

from session_agent import SessionAgent
from base_handler import BaseHandler
from db_connector import DBConnector
import time
import datetime

expert_main = 'http://127.0.0.1:8890'
researcher_main = 'http://127.0.0.1:8891'

class AllNewsHandler(tornado.web.RequestHandler):
	def __get_prev_days__(self, n_days):
		prev_day = datetime.datetime.now() - datetime.timedelta(days=n_days)
		prev_date_str = prev_day.strftime("%Y-%m-%d %H:%M:%S")
		prev_time_tuple = time.strptime(prev_date_str, "%Y-%m-%d %H:%M:%S")

		return time.gmtime(time.mktime(prev_time_tuple))

	def get(self):
		db_conn = DBConnector()

		after_time = self.__get_prev_days__(15)
		news_items = db_conn.after_date_news(after_time)

		to_render = []
		for n in news_items:
			to_render.append("Title: {} \nSummary: {}".format(n['title'], n.get('summary', "none")))

		self.render("all_news.html", title="recent news", items=to_render)

class IDHandler(tornado.web.RequestHandler):
	def get(self, id_item):
		self.write("requested news item with id = " + id_item)
#---------------------------------------------------------------

class LoginHandler(BaseHandler):
	def get(self):
		if self.get_current_user():
			self.redirect("/logout")
			return
		self.render("login.html")

	def post(self):
		user_data = {}
		user_data['username'] = self.get_argument('username', '')
		user_data['password'] = self.get_argument('password', '')

		if	not user_data['username'] or \
			not user_data['password']:
			self.redirect("/login")
			return

		s_agent = SessionAgent()
		resp = s_agent.self_login_user(user_data)
		if resp.status == 202:
			cookie = json.loads(resp.data.decode('utf-8'))
			self.set_cookie('user_cookie', cookie['user_cookie'])
			self.redirect("/")
			return

		msg = resp.reason
		print 'INF: user {} is not logged in: {}'.format(user_data['username'], resp.reason)
		self.redirect('/auth')

class LogoutHandler(BaseHandler):
	def get(self):
		if not self.get_current_user():
			self.redirect("/")
			return

		self.render("logout.html")

	def post(self):
		user_cookie = self.get_current_user()
		if not user_cookie:
			self.redirect("/")
			return

		s_agent = SessionAgent()
		resp = s_agent.self_logout_user({'user_cookie': user_cookie})
		self.clear_cookie('user_cookie')
		self.redirect("/")

class RegisterHandler(BaseHandler):
	def get(self):
		if self.get_current_user():
			self.redirect("/logout")
			return
		self.render("register.html")

	def post(self):
		user_data = {}
		user_data['name'] = self.get_argument('name', '')
		user_data['surname'] = self.get_argument('surname', '')
		user_data['username'] = self.get_argument('username', '')
		user_data['password'] = self.get_argument('password', '')
		user_data['role'] = self.get_argument('role', '')

		for k, v in user_data.items():
			if not v:
				self.redirect("/register")
				return

		s_agent = SessionAgent()
		resp = s_agent.register_user(user_data)

		msg = 'Successfull registration'
		if resp.status != 201:
			msg = resp.reason
		self.render("end_of_user_reg.html", msg=msg)

class AuthHandler(BaseHandler):
	def get(self):
		if self.get_current_user():
			self.redirect("/")
			return
		self.render("auth.html")

	def post(self):
		if self.get_argument('login', '') != '':
			self.redirect("/login")
			return
		if self.get_argument('register', '') != '':
			self.redirect("/register")
			return
		raise tornado.web.HTTPError(500)

class MainHandler(BaseHandler):
	def get(self):
		cookie = self.get_current_user()
		if not cookie:
			self.redirect("/auth")
			return

		s_agent = SessionAgent()
		resp = s_agent.get_role_by_cookie({'user_cookie': cookie})
		if resp.status != 200:
			self.send_error(500)

		role_info = json.loads(resp.data.decode('utf-8'))
		if role_info['id'] == 1:
			self.redirect(expert_main)
		elif role_info['id'] == 2:
			self.redirect(researcher_main)
		else:
			self.write("Welcome to news rating system!")

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/auth", AuthHandler),
	(r"/login", LoginHandler),
	(r"/logout", LogoutHandler),
	(r"/register", RegisterHandler),
	(r"/all_news", AllNewsHandler),
	(r"/id/([0-9]+)", IDHandler)
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
