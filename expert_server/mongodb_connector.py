import pymongo
from pymongo import MongoClient
import random

class MongoConnector():
	def __init__(self, host='localhost', port=27017, debug=False):
		self.client = None
		self.debug = debug

		self.__connect__(host, port)
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

	def insert_interview(self, interview_data):
		if	'title' not in interview_data.keys() or \
			'articles' not in interview_data.keys():
			print 'W: incorrect interview data'
			return None

		try:
			interview = self.db.interview
			interview_id =  interview.insert_one(interview_data).inserted_id
			print 'DEB: inserted interview (id={})'.format(interview_id)
			return interview_id
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def get_interview_cnt(self):
		try:
			return self.db.interview.count()
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def insert_interview(self, interview_el):
		try:
			return self.db.interview.insert_one(interview_el).inserted_id
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def get_n_news(self, n):
		try:
			news = self.db.news_item
			news_data = news.find()

			res = set()
			res_news = []
			for i in range(n):
				rand = random.randrange(n)
				while rand in res:
					rand = random.randrange(n)
				res.add(rand)
				res_news.append(news_data[rand])

			return res_news
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None


