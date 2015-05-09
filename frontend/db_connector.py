from pymongo import MongoClient
import datetime

class DBConnector():
	def __init__(self, host='localhost', port=27017, debug=False):
		self.client = None
		self.debug = debug
		self.db = None

		if self.__connect__(host, port):
			self.db = self.client.news_db

	def __connect__(self, host, port):
		if self.client is not None:
			self.client.close()
		try:
			self.client = MongoClient(host, port)
			return True
		except pymongo.errors.ConnectionFailure:
			print("ERR: mongodb: connection to db failed")
			return False

	# XXX: after_date is datetime object
	def after_date_news(self, after_date):
		if self.db is None:
			return None

		print("INF: fetch news after date {}".format(after_date))
		news_items = []
		for r in self.db.news_item.find({	'published_parsed': {'$gte': after_date} }):
			news_items.append(r)

		return news_items
