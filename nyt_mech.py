import json
import urllib
import mechanize
from mechanize._beautifulsoup import BeautifulSoup
import re
import string
import pickle

import pdb
import pprint

# API keys
api_article = "b59cddc734e6cbc7bf3743afdc2b0a81:10:61317310"
api_newswire = "49de2f92ea250186754c1d5d616c169e:19:61317310"

#types = ["Top/News/"+m for m in ["World","Science","U.S.","Washington","Business","Health","Science"]]

host = "api.nytimes.com"
path = "/svc/search/v1/article"

month = {"fee":"N ",
         "material_type_facet":"[News]",
         "publication_month":"[01]",
         "publication_year":"[2010]",
         "classifiers_facet":"["+"Top/News"+"]"}
args = {"format":"json",
        "query":"".join([k+":"+v for (k,v) in month.iteritems()]),
        "fields":"title,url,word_count,classifiers_facet,des_facet,fee",
        "offset":"0",
        "api-key":api_article}

br = mechanize.Browser()
punct = "".join(["\m" for m in string.punctuation])

def grab_article(url):
    br.open(url)
    soup = BeautifulSoup(br.response().get_data().strip())
    article = soup("div",{"class":"articleBody"})
    a = article.pop()
    b = re.sub(r'(\<.*\>|\s|\&.{1,5}\;|\.|\,|'+punct+')',' ',str(a))
    return b.lower()

def tokenize(page):
    tokens = page.split(" ")
    tokens = [x for x in tokens if len(x)>2]
    return set(tokens)

def update(corpus,tokens,mult=1):
    for t in tokens:
        corpus[t] = corpus.get(t,0)+mult

url = "http://"+host+path+"?"+urllib.urlencode(args.items())

br.open(url)
data = json.loads(br.response().get_data())

story = data["results"][0]
article = grab_article(story["url"])

