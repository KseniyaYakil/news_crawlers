from html.parser import HTMLParser

class Tag():
	# attrs = [{key: val}]
	def __init__(self, tag='', attrs=None):
		self.tag = tag
		self.attrs = []
		if attrs is not None:
			self.attrs = attrs
		self.data = ""

class FeedHTMLParser(HTMLParser):
	def __init__(self):
		super(FeedHTMLParser, self).__init__(convert_charrefs=True)
		self.article = {	'name': Tag(tag='h2', attrs=[('class', 'article_name')]),
							'sub_header': Tag(tag='h1', attrs=[('class', 'article_subheader')]),
							'text': Tag(tag='p', attrs=[('class', 'b_article__text')]),
							'intro': Tag(tag='span', attrs=[('class', 'b_article__intro')]) }
		self.level_tags = []

	def handle_starttag(self, tag, attrs):
		# Parse article info
		print("Processing tag {}..".format(tag))
		for (param, p_tag) in self.article.items():
			if p_tag.tag == tag:
				all_attr_found = False
				for (a_name, a_val) in p_tag.attrs:
					found = False
					for (t_name, t_val) in attrs:
						if a_name == t_name:
							if t_val == a_val:
								found = True
							break

					if found == False:
						all_attr_found = False
						break
					else:
						all_attr_found = True
				if all_attr_found:
					print("Add tag {}".format(p_tag.tag))
					self.level_tags.append(p_tag)
					return
		self.level_tags.append(None)

	def handle_data(self, data):
		if self.level_tags[-1] is None:
			return
		print("Tag {} data {}".format(self.level_tags[-1].tag, data))
		self.level_tags[-1].data = data

	def handle_endtag(self, tag):
		lev_tag = self.level_tags.pop()
		if lev_tag is not None:
			print("End of tag {}".format(lev_tag.tag))


