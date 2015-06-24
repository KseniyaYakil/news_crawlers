import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
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

	def get_interview(self, obj_id):
		try:
			interview_info = self.db.interview.find_one({'_id': ObjectId(obj_id)})
			res = {	'name': interview_info['name'],
					'_id': interview_info['_id'],
					'news': []}
			for n in interview_info['news']:
				news_item = self.db.news_item.find_one({'_id': ObjectId(n['id'])})
				news_item['score'] = n['score']
				news_item['appraisal_cnt'] = n['appraisal_cnt']
				res['news'].append(news_item)
			return res
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

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

	def get_all_interviews(self):
		try:
			all_interviews = self.db.interview.find()
			res = []
			for i in all_interviews:
				res.append(i)

			return res
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def get_interview_articles(self, obj_id):
		try:
			interview = self.db.interview.find_one({'_id': ObjectId(obj_id) })
			news_items = []
			for n in interview['news']:
				news_i = self.db.news_item.find_one({'_id': ObjectId(n['id'])})
				news_items.append(news_i)
			return news_items
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def insert_interview(self, interview_el):
		try:
			return self.db.interview.insert_one(interview_el).inserted_id
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def update_interview(self, obj_id, news_items):
		try:
			for n_item in news_items:
				print 'news item {}'.format(n_item)
				news_item_id = n_item['id']
				if n_item['selection'] == 'good':
					score = 1
				else:
					score = 0
				print 'DEB: obj_id {} news_item_id {} score {}'.format(obj_id, news_item_id, score)
				self.db.interview.update(	{"$and": [	{"_id": ObjectId(obj_id)},
														{"news": {"$elemMatch": { "id": ObjectId(news_item_id)}}}]},
											{"$inc": {"news.$.score": int(score), "news.$.appraisal_cnt": int(1)}})
		except Exception as ex:
			print 'ERR: {}'.format(ex)

	def get_n_news(self, n):
		try:
			news = self.db.news_item
			news_data = news.find()
			news_cnt = news.count()

			res = set()
			res_news = []
			for i in range(n):
				rand = random.randrange(news_cnt)
				while rand in res:
					rand = random.randrange(news_cnt)
				res.add(rand)
				res_news.append(news_data[rand])

			return res_news
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None


