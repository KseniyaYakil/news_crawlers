#encoding=utf-8
from math import ceil

class Pagination(object):
    def __init__(self, items, page, per_page=20):
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = len(items)
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        return int(ceil(self.total / float(self.per_page)))

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    def __get_page_items__(self, page_low_limit, page_numb):
        assert self.items is not None
        if self.page < page_low_limit:
            return None
        start_pos = self.per_page * page_numb
        end_pos = start_pos + self.per_page

        if start_pos >= len(self.items):
            return None

        if end_pos > len(self.items):
            end_pos = len(self.items)

        return self.items[start_pos : end_pos]

    def prev(self):
        return self.__get_page_items__(2, self.page - 2)

    def next(self):
        return self.__get_page_items__(2, self.page)

    def cur_page_items(self):
        return self.__get_page_items__(1, self.page - 1)

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:
        .. sourcecode:: html+jinja
            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
