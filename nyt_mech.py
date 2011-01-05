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
        "fields":"title,url,word_count,classifiers_facet,des_facet,abstract,fee",
        "offset":"0",
        "api-key":api_article}

br = mechanize.Browser()
punct = "".join(["\m" for m in string.punctuation])

def grab_meta(res):
    meta = " ".join([res.get("title","")," ".join(res.get("des_facet",[]))])
    meta += " "+" ".join([s[4:] for s in res.get("classifiers_facet")])
    meta += res.get("abstract","")
    return meta

def grab_article(url):
    br.open(url)
    soup = BeautifulSoup(br.response().get_data().strip())
    article = soup("div",{"class":"articleBody"})
    a = article.pop()
    return str(a)

class BayesFilter:
    pcorpus = {}
    ncorpus = {}
    pcount = 0
    ncount = 0
    multiple  = 1 # number of times to insert

    def __init__(self,mult=1):
        self.mult = mult

    def tokenize(self,page):
        # do sanitization here
        p = re.sub(r'(\<.*\>|\s|\&.{1,5}\;|\.|\,|'+punct+')',' ',page)
        p = p.lower()
        tokens = p.split(" ")
        tokens = [x for x in tokens if len(x)>2]
        return set(tokens)
    
    def det(self,page):
        tokens = self.tokenize(page)
        prob  = 0.5
        nprob = 0.5
        for w in tokens:
            p = self.pcorpus.get(w,0)
            n = self.ncorpus.get(w,0)
            if p+n < 1:
                continue
            tempprob = p/float(p+n)
            prob *= tempprob    # I don't like this method, check this
            nprob *= 1-tempprob
        return prob/(prob+nprob)

    def update(self,page,scale):
        '''scale: 0-1, mult: how many times to count'''
        tokens = self.tokenize(page)
        for t in tokens:
            self.pcorpus[t] = self.pcorpus.get(t,0)+scale*self.mult
            self.ncorpus[t] = self.ncorpus.get(t,0)+(1-scale)*self.mult

    def upvote(self,page):
        '''Shortcut fns for update'''
        self.update(page,1)
    def downvte(self,page):
        '''Shortcut fns for update'''
        self.update(page,0)

    def unload(self,path="filter.db"):
        f = open(path)
        pickle.dump([self.pcorpus,self.ncorpus,self.mult],f)

    def load(self,path="filter.db"):
        f = open(path)
        [self.pcorpus,self.ncorpus,self.mult] = pickle.load(f)

bf = BayesFilter()

# tiny trainer
while True:
    url = "http://"+host+path+"?"+urllib.urlencode(args.items())
    br.open(url)
    resp = json.loads(br.response().get_data())
    res = resp["results"]

    for r in res:
        print r.get("title","No title")
        print r.get("des_facet","No description")
        print r.get("abstract","No abstract")
        print r.get("url")
        print bf.det(grab_meta(r))
        print "y/n? ",
        bf.update(grab_meta(r),{'y':1,'n':0}[raw_input()])
        
    args["offset"] = str(int(args["offset"])+1)

