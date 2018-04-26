import sys, requests
from html.parser import HTMLParser

interesting = {
    'data-page-title':'',
    'data-article-title':'',
    'data-article-image':'',
    'data-authors':'',
    'data-article-description':'',
    'data-article-image':'',
    'data-article-publish-date':'',
    'data-article-publish-time':'',
    'data-is-premium':'',
    'data-access-locked':'',
    'article__body':'',
    'article__lead':'',
    'article__body-content':'',
}
my_tags = ['p','h1']

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.found_article = False
        self.found_body = False
        self.parse_content = False
        self.article = {'body':[],'description':''}
        HTMLParser.__init__(self)
        
    
    def handle_starttag(self, tag, attrs):
        if not self.found_article and tag == 'div':
            #print("Possible start of article parsing on tag: ", tag)
            for attr in attrs:
                if self.found_article:
                    if attr[0] in interesting:
                        self.article[attr[0]] = attr[1]
                elif attr[1] == 'js-article':
                    #print("Found start of parsing tag via attr: ", attr)
                    self.found_article = True
        elif not self.found_body and tag == 'div':
            #print("Possible start of body parsing on tag: ", tag)
            for attr in attrs:
                if attr[1] == 'article__body':
                    #print("Found start of body parsing tag via attr: ", attr)
                    self.found_body = True
            
        elif self.found_body and tag == 'p':
            self.parse_content = True            
            
            

    def handle_endtag(self, tag):
        #print("Encountered an end tag : ", tag)
        if tag == 'p':
            parse_content = False
        elif tag == 'main':
            self.found_body = False

    def handle_data(self, data):
        if self.found_body and self.parse_content:
            self.article['body'].append(data)
            #print("Want to parse this data: ", data)

    def write_article(self):
        #print(self.article)
        page_title = self.article['data-page-title']
        article_title = self.article['data-article-title']
        img_url = self.article['data-article-image'] if 'data-article-image' in self.article else ''
        print(img_url)
        filename = page_title.replace(' ', '_').lower() + '.html'

        with open(filename, 'w') as f:
            f.write('<html>\n<head>\n')
            f.write('<link rel=\"stylesheet\"')
            f.write('href=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css\">\n')
            f.write('<title>{}</title>\n</head>\n'.format(page_title))
            f.write('<body><div class="container">\n<h1>{}</h1>\n'.format(article_title))
            if len(img_url) > 0:
                f.write('<img class=\"responsive-img\" src=\"{}\">'.format(img_url))

                
            text = ''
            for item in self.article['body']:
              #  if len(item.replace(' ','')) != 0:
                text += item
            f.write('<p class="flow-text">{}</p>\n'.format(text))
            f.write('</div></body>\n</html>')
            
def main():
    if len(sys.argv) < 2:
        print('Usage: python3 scrape_dn.py urls')
    else:
        urls = sys.argv[1:]
        for url in urls:
            r = requests.get(url)
            if r.status_code is 200:
                parser = MyHTMLParser()
                parser.feed(r.text)
                parser.write_article()
                parser.close()
            else:
                print('Request failed on url %, status code %', url, r.status_code)
            
if __name__ == "__main__":
    main()


#Fixa något intuitivt taggningssystem för taggar vi inte vill ha, t.ex. taggnamn på "prenumera dn"
#Fixa in filmer och slideshows
#Snygga till texten
#Centrering
#
