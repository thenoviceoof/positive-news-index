import json
import urllib
import urllib2
import pprint
import BeautifulSoup

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

import pdb

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
def grab_article(url):
    request = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15'})
    data_string = opener.open(request).read()
    #pdb.set_trace()
    page = BeautifulSoup.BeautifulSoup(data_string)
    article = page.find("div",{"class":"articleBody"})
    return page

url = "http://"+host+path+"?"+urllib.urlencode(args.items())

page = urllib2.urlopen(url)
data_string = page.read()
data = json.loads(data_string)

story = data["results"][0]
article = grab_article(story["url"])
