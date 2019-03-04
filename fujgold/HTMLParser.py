import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    INTERESTING_TAG = 'table'

    def __init__(self):
        self.res = []
        self.temp_res = []
        self.do_print = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == MyHTMLParser.INTERESTING_TAG:
            self.do_print = True

        if tag == 'tr' and self.do_print:
            self.temp_res = []

    def handle_endtag(self, tag):
        if tag == MyHTMLParser.INTERESTING_TAG:
            self.do_print = False

        if tag == 'tr' and self.do_print:
            self.res.append(self.temp_res)

    def handle_data(self, data):
        data = data.strip()
        data = re.sub(r"\s+", " ", data)
        if self.do_print and data:
            self.temp_res.append(data)