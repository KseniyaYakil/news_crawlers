from news_parser import BaseNewsParser

class ChaskorParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(ChaskorParser, self).__init__(config, debug)

		self.opt_for_items['text'] = {'field': 'yandex_full-text'}
		self.text_extr_fields.add('text')
		self.news_agent_name = "частный корреспондент"

	def __get_article_from_html__(self, news_item, web_page):
		if 'text' in news_item.keys():
			news_item['web_page'] = news_item['text']
			del news_item['text']
			return
		# parse web page
