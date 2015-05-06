from news_parser import BaseNewsParser

class KommersantParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(KommersantParser, self).__init__(config, debug)

