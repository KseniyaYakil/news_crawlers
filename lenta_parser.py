from news_parser import BaseNewsParser

class LentaParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(LentaParser, self).__init__(config, debug)
		self.news_agent_name = "лента"

