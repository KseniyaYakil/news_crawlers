from html.parser import HTMLParser

""" Extracts all text data between each <tag> and </tag>
	in feed and then concatinates all texts between tags """
class CutHTML(HTMLParser):
	def __init__(self):
		super(CutHTML, self).__init__(convert_charrefs=True)
		self.extr_data = ""

	def reset(self):
		super(CutHTML, self).reset()
		self.extr_data = ""

	def handle_data(self, data):
		self.extr_data += " " + data

	def get_data(self):
		return self.extr_data
