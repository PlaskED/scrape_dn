import os, requests
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.parse = False
    
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
        if tag is 'div' and 'js-article' in attrs:
            parse = True

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
        if parse:
            parse = False

    def handle_data(self, data):
        #print "Encountered some data  :", data
        

if len(os.argv) is not 2:
    print('Usage: python3 scrape_dn.py url')
    return 1

r = requests.get(os.argv[1])
if r.status_code is 200:
    parser = MyHTMLParser()
    parser.feed(r.text)

    parser.close()
    
else:
    print('Request failed, status code %', r.status_code)
    return 1
        
