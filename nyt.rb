# API keys
article = "b59cddc734e6cbc7bf3743afdc2b0a81:10:61317310"
newswire = "49de2f92ea250186754c1d5d616c169e:19:61317310"

require 'net/http'
require 'uri'
require 'open-uri'
require 'rubygems'
require 'json'
require 'nokogiri'

types = ["World","Science","U.S.","Washington","Business","Health","Science"].map{|m| "[Top/News/"+m+"]"}
#"Front Page",,

proto = nil
host = "api.nytimes.com"
port = nil
path = "/svc/search/v1/article"

args = {"format"=>"json",
  "query"=>"publication_month:[01]publication_year:[2010]classifiers_facet:"+types[0],
  #"fields"=>"url,word_count,classifiers_facet",
  "fields"=>"title,classifiers_facet",
  "offset"=>"0",
  "api-key"=>article}

u = URI::HTTP.build([proto,host,port,path,args.map{|n,v|n+"="+v}.join("&"),nil])

r = Net::HTTP.get u
puts r
j = JSON.parse(r)

#u = URI.parse(j['results'][0]["url"])
#r = Net::HTTP.get u
#h = Nokogiri::HTML(r)
