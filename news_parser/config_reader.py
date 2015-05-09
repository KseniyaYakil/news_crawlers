
import os.path
import re

class ConfigReader():
	def __init__(self):
		self.url_names = []
		self.freq = -1
		self.url_matcher = re.compile(r"(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|"\
							"[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"\
							"\s+(?P<term>(?:\'[\s\w]+\')+)?")
		self.main_matcher = re.compile(r"(rss_list\s+(?P<rss_list>[\w\._-]+))|"\
										"(freq\s+(?P<freq>\d+))")

	def read(self, config_file, debug=False):
		if	config_file is None or					\
			os.path.isfile(config_file) == False or \
			os.access(config_file, os.R_OK) == False:
			print("ERR: unable to read config file")
			return -1

		with open(config_file, mode='r', encoding='utf-8') as cfg_file:
			for line in cfg_file:
				result = self.main_matcher.match(line)
				if result is None:
					continue
				if result.group('rss_list') is not None:
					self.__get_urls_names__(result.group('rss_list'), debug)
					continue
				if result.group('freq') is not None:
					self.freq = int(result.group('freq'))

	def __get_urls_names__(self, config_file, debug=False):
		self.url_names = []
		if	config_file is not None and \
			os.path.isfile(config_file) and \
			os.access(config_file, os.R_OK):
			with open(config_file, mode='r', encoding='utf-8') as cfg_file:
				for line in cfg_file:
					if debug:
						print("Line {}".format(line))
					result = self.url_matcher.match(line)

					if result is None:
						continue
					info = {'url': result.group('url'),
							'term': ''}
					if result.group('term') is not None:
						info['term'] = str(result.group('term')).replace('\'', '')

					if debug:
						print("Config: {}".format(info))
					self.url_names.append(info)
		else:
			print("ERR: unable to read config file {}".format(config_file))
