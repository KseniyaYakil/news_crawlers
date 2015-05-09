#!/usr/bin/python

import tornado.ioloop
import tornado.web
from db_connector import DBConnector
import time
import datetime

class MainHandler(tornado.web.RequestHandler):
	def __get_prev_days__(self, n_days):
		prev_day = datetime.datetime.now() - datetime.timedelta(days=n_days)
		prev_date_str = prev_day.strftime("%Y-%m-%d %H:%M:%S")
		prev_time_tuple = time.strptime(prev_date_str, "%Y-%m-%d %H:%M:%S")

		return time.gmtime(time.mktime(prev_time_tuple))

	def get(self):
		db_conn = DBConnector()

		after_time = self.__get_prev_days__(1)
		news_items = db_conn.after_date_news(after_time)

		to_render = []
		for n in news_items:
			to_render.append("Title: {} \nSummary: {}".format(n['title'], n.get('summary', "none")))

		self.render("all_news.html", title="recent news", items=to_render)

class IDHandler(tornado.web.RequestHandler):
	def get(self, id_item):
		self.write("requested news item with id = " + id_item)

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/id/([0-9]+)", IDHandler)
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
