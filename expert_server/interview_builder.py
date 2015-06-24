import sys
sys.path.append("../util")
from mongodb_connector import MongoConnector

class InterviewBuilder():
	def __init__(self, debug=False):
		self.debug = debug
		self.news_per_interview = 3
		self.interview_limit = 10
		self.db_conn = MongoConnector(debug=self.debug)

	def create_new_interviews(self):
		interview_cnt = self.db_conn.get_interview_cnt()
		print 'DEB: interview cnt {}'.format(interview_cnt)
		if interview_cnt >= self.interview_limit:
			return

		news_items = self.db_conn.get_n_news(self.news_per_interview)

		interview = {}
		interview['name'] = 'interview_{}'.format(interview_cnt)
		interview['news'] = []
		for n in news_items:
			add_news_item = {
				'id': n['_id'],
				'score': 0,
				'appraisal_cnt': 0
			}
			print 'add news item: {}'.format(add_news_item)
			interview['news'].append(add_news_item)

		self.db_conn.insert_interview(interview)
