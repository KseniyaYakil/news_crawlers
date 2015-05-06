from news_parser import BaseNewsParser

class RIAParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(RIAParser, self).__init__(config, debug)
