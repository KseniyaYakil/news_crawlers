#!/usr/bin/python
from optparse import OptionParser
import time

from news_parser import *
from chaskor_parser import ChaskorParser
from kommersant_parser import KommersantParser
from ria_parser import RIAParser
from lenta_parser import LentaParser

def parse_options():
		parser = OptionParser()
		parser.add_option("-d", "--debug", dest="debug",
						help="debug mode", action="store_true")
		parser.add_option(
						"-c", "--config", dest="config",
						help="configuration file")
		parser.add_option(
						"-t", "--type", dest="type_parser",
						type="int",
						help="type of parser:	\
								0 - Chaskor,	\
								1 - Kommersant,	\
								2 - RIA,		\
								3 - Lenta")

		(opt, args) = parser.parse_args()
		if opt.config is None or opt.type_parser is None:
			parser.print_help()
			return None
		return opt

def main():
		opt = parse_options()
		if opt is None:
				return

		news_parser = None
		if opt.type_parser == 0:
			news_parser = ChaskorParser(config=opt.config, debug=opt.debug)
		if opt.type_parser == 1:
			news_parser = KommersantParser(config=opt.config, debug=opt.debug)
		if opt.type_parser == 2:
			news_parser = RIAParser(config=opt.config, debug=opt.debug)
		if opt.type_parser == 3:
			news_parser = LentaParser(config=opt.config, debug=opt.debug)

		#feed_list = news_parser.get_feed_list(url='http://ria.ru/export/rss2/politics/index.xml')

		# +0000
		#time_mark = time.strptime("Tue May 05 09:40:00 2015")

		#news_after_date = news_parser.filter_by_time(feed_list, time_mark)

		news_parser.fetch_all_feed_lists()
		#all_feed_data = news_parser.fetch_news_by_feed_list(feed_list)

if __name__ == '__main__':
		main()
