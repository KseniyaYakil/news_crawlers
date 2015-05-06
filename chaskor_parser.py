from news_parser import BaseNewsParser

class ChaskorParser(BaseNewsParser):
	def __init__(self, config='', debug=False):
		super(ChaskorParser, self).__init__(config, debug)

		self.opt_for_items['text'] = {'field': 'yandex_full-text'}
		self.text_extr_fields.add('text')
