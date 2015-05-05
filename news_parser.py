#!/usr/bin/python
import feedparser

from config_reader import ConfigReader
from connector import Connector
from html_feed_parser import Tag, FeedHTMLParser

# from RSS 
class BaseNewsParser:
	def __init__(self, config=None, debug=False):
		self.req_fields = ['title', 'descriprion', 'link']
		self.opt_for_feed = {	'language': "",					\
								'subtitle': "",					\
								'pubDate': "",					\
								'updated': "",					\
								'updated_parsed': "",			\
								'lastBuildDate': "",			\
								'SkipHours': "",				\
								'SkipDays': "",		}

		self.opt_for_items = {	'published': "",				\
								'published_parsed': "",			\
								'pubDate': "",					\
								'source': "",					\
								'language': "",					\
								'category': "",					\
								'term': {	'field': 'tags',	\
											'sub_field': 'term'},\
								'author': "",					\
								'summary': ""				}
		self.html_parser = FeedHTMLParser()
		self.debug = debug

		self.rss_urls = ConfigReader.get_urls_names(config, self.debug)

	def __set_required_fields__(self, news_item, feed, keys):
		for key in keys:
			if key not in feed.keys():
				continue

			news_item[key] = feed[key]

	def __set_opt_fields__(self, news_item, feed, dict_keys):
		for (key, val) in dict_keys.items():
			if val == "":
				if key in feed.keys():
					news_item[key] = feed[key]
			elif val['field'] != None:
				if val['field'] not in feed.keys():
					continue

				feed_var = feed[val['field']]
				if isinstance(feed_var, str):
					if val.get('sub_field', None):
						print("ERR: expect sub_field {} in {}".format(val['sub_field'], val['field']))
						continue
					news_item[key] = feed_var

				if isinstance(feed_var, list):
					feed_var = feed_var[0]

				if isinstance(feed_var, dict):
					if val.get('sub_field', None) is None or val['sub_field'] not in feed_var.keys():
						print("ERR: no sub_field in {} or sub_field not in feed".format(val['field']))
						continue
				news_item[key] = feed_var[val['sub_field']]

	def __form_news_list__(self, rss_news):
		# Parse news_agent data 
		news_agent_data = dict()
		self.__set_required_fields__(news_agent_data, rss_news.feed, self.req_fields)
		self.__set_opt_fields__(news_agent_data, rss_news.feed, self.opt_for_feed)

		if self.debug:
			print("Print news.feed")
			for (k, v) in rss_news.feed.items():
				print("{} -> {}".format(k, v))

			print("\nStoring feed info")
			for (k, v) in news_agent_data.items():
				print("{} -> {}".format(k, v))

			print("\nPrint [0] news item:")
			for (k, v) in rss_news.entries[0].items():
				print("{} -> {}".format(k, v))

		# Parse each news item
		news = []
		for n in rss_news.entries:
			news_item = dict()
			self.__set_required_fields__(news_item, n, self.req_fields)
			self.__set_opt_fields__(news_item, n, self.opt_for_items)

			news.append(news_item)

			if self.debug:
				print("\nadding news item: ")
				for (k, v) in news_item.items():
					print("{} -> {}".format(k, v))

		return {'news_agent': news_agent_data,
				'news_items': news}


	def fetch_news_by_feed_list(self, news_data):
		conn = Connector()
		for n in news_data['news_items']:
			# TODO: check if link is valid?
			print("Fetching news page for '{}'".format(n['link']))
			news_item_page = conn.get(url=n['link'])
			n['web_page'] = news_item_page.data
			#print("Web page {}".format(news_item_page.data))

		# FIXME: handle with encoded data
		#self.html_parser.reset()
		#self.html_parser.feed(n['web_page'])


	def get_feed_list(self, url=None):
		if url is None:
			if self.news_url is None:
				print("ERR: unable to fetch news (no url)")
				return None
			url = self.news_url
		try:
			print("Request RSS from '{}'".format(url))
			rss_news = feedparser.parse(url)
			print("RSS data recieved")

			return self.__form_news_list__(rss_news)
		except Exception as exp:
			print("ERR: {}".format(exp))
			return None

	# Fetch feed lists according to config urls
	def fetch_all_feed_lists(self):
		if len(self.rss_urls) == 0:
			print("ERR: unable to fetch all feed lists: no feed lists")
			return -1

		for rss_url in self.rss_urls:
			news_data = self.get_feed_list(rss_url['url'])

class ChaskorParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(ChaskorParser, self).__init__(debug)

		self.opt_for_items['text'] = {'field': 'yandex_full-text'}
		self.news_url = 'http://www.chaskor.ru/rss.php'

class KommersantParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(KommersantParser, self).__init__(config, debug)

		self.news_url = 'http://www.kommersant.ru/RSS/daily.xml'

