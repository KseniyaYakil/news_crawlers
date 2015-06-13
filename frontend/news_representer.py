#!/usr/bin/python

import tornado.ioloop
import tornado.web
from db_connector import DBConnector
import time
import datetime

class AllNewsHandler(tornado.web.RequestHandler):
	def __get_prev_days__(self, n_days):
		prev_day = datetime.datetime.now() - datetime.timedelta(days=n_days)
		prev_date_str = prev_day.strftime("%Y-%m-%d %H:%M:%S")
		prev_time_tuple = time.strptime(prev_date_str, "%Y-%m-%d %H:%M:%S")

		return time.gmtime(time.mktime(prev_time_tuple))

	def get(self):
		db_conn = DBConnector()

		after_time = self.__get_prev_days__(60)
		news_items = db_conn.after_date_news(after_time)

		to_render = []
		for n in news_items:
			to_render.append("Title: {} \nSummary: {}".format(n['title'], n.get('summary', "none")))

		self.render("all_news.html", title="recent news", items=to_render)

class IDHandler(tornado.web.RequestHandler):
	def get(self, id_item):
		self.write("requested news item with id = " + id_item)
#---------------------------------------------------------------

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		# TODO: check cookie 
		return None

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		if self.current_user:
			self.redirect("/logout")
		self.render("login.html")

	def post(self):
		username = self.get_argument('username', '')
		password = self.get_argument('password', '')

		if not username or not password:
			self.redirect("/login")
			return
		self.write("your username {} and password {}".format(username, password))

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		if not self.current_user:
			self.redirect("/")
		self.render("logout.html")

	def post(self):
		if not self.current_user:
			self.redirect("/")

		# TODO: log out there
		self.write("Log out there")

class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		if self.current_user:
			self.redirect("/logout")
		self.render("register.html")

	def post(self):
		user_data = {}
		user_data['name'] = self.get_argument('name', '')
		user_data['surname'] = self.get_argument('surname', '')
		user_data['username'] = self.get_argument('username', '')
		user_data['password'] = self.get_argument('password', '')

		for k, v in user_data.items():
			if not v:
				self.redirect("/register")
				return

		self.write("you reg data {}".format(user_data))

class AuthHandler(tornado.web.RequestHandler):
	def get(self):
		if self.current_user:
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

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		if not self.current_user:
			self.redirect("/auth")
			return
		# TODO: foreach user role show different home pages
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
