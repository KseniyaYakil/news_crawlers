#!/usr/bin/python
from news_parser import *

# get main page -> find out wich url is for rss news format

def main():
		#news_parser = ChaskorParser(debug=True)
		news_parser = KommersantParser(config='kommersant.conf', debug=True)
		feed_list = news_parser.get_feed_list()
		news_parser.fetch_all_feed_lists()
		#all_feed_data = news_parser.fetch_news_by_feed_list(feed_list)

if __name__ == '__main__':
		main()
