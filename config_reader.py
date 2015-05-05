
import os.path
import re

class ConfigReader():
	def get_urls_names(config_file, debug=False):
		urls_names = []
		if config_file is not None and \
			os.path.isfile(config_file) and \
			os.access(config_file, os.R_OK):
			with open(config_file, mode='r', encoding='utf-8') as cfg_file:
				m = re.compile(r"(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\s+(?P<term>(?:\'[\s\w]+\')+)?")
				for line in cfg_file:
					print("Line {}".format(line))
					result = m.match(line)

					if result is None:
						continue
					info = {'url': result.group('url'),
							'term': ''}
					if result.group('term') is not None:
						info['term'] = str(result.group('term')).replace('\'', '')

					if debug:
						print("Config: {}".format(info))
					urls_names.append(info)
		else:
			print("ERR: unable to read config file {}".format(config_file))

		return urls_names
