#!/usr/bin/python
 
import os
import sys
 
libpath = os.getcwd() + os.sep
sys.path.extend([libpath + 'lib/python2.6', libpath + 'bin'])
 
from bottle import request, route
import bottle
from wsgiref.handlers import CGIHandler
 
import ConfigParser
import urllib2
from urllib2 import URLError
from urllib import quote_plus
 
@route('/')
def index():
    return "OK"
 
@route('/hello/:name')
def hello(name):
    return "Hello %s" % (name)
 
@route('/search/:keyword')
def search(keyword):
    url = host + "/Search/term/%s?key=%s" % (quote_plus(keyword), key)
    try:
        response = urllib2.urlopen(url)
        out = ""
        for line in response:
            out += line
        return "<pre>" + str(out) + "</pre>"
    except URLError as e:
        return "<font color=\"red\">Error: %s</font>" % (str(e))

@route('/searchsize/:keyword', method="POST")
def searchsize(keyword):
    # out = "request.forms: " + str(request.forms.items()[0])
    infields = request.json
    out = ""
    sex = infields['gender']
    request_facets = {}
    if sex == 'Mens':
        for facet in mens_facets:
            if facet in infields:
                request_facets[facet] = infields[facet]
    elif sex == 'Womens':
        for facet in womens_facets:
            if facet in infields:
                request_facets[facet] = infields[facet]
    for facet in universal_facets:
        if facet in infields:
                request_facets[facet] = infields[facet]
    #out += "facets: " + str(request_facets)
    url = host + '/Search/term/%s?filters=%s&includes=["colorFacet","gender","priceFacet","size","sizegroup"]&key=%s' % (quote_plus(keyword), build_facets(request_facets), key)
    try:
        response = urllib2.urlopen(url)
        #out += "/* <b>REQUEST</b><br/><pre>" + url + "</pre><p/><b>RESPONSE</b><br/><pre> */\n"
        for line in response:
            out += line
        return out #+ "</pre>"
    except URLError as e:
        #return "<font color=\"red\">Error: %s</font>\n%s" % (str(e), url)
        return "{'ERROR':'%s %s'}" % (str(e), url)

def build_facets(request_facets):
    map = {}
    for facet in request_facets:
        value = request_facets[facet]
        if type(value) == str:
            map['"' + facet + '"'] = '["' + value + '"]'
        elif type(value) == list:
            values = []
            for elem in value:
                values.append('"' + elem + '"')
            map['"' + facet + '"'] = '[' + ",".join(values) + ']'
        
    out = "{"
    for key in map:
        if len(out) > 1:
            out += ","
        out += key + ":" + map[key]
    return out + "}"
    
mens_facets = [    
"hc_men_apparel_blazer_size",
"hc_men_apparel_bottom_belt_size",
"hc_men_apparel_bottom_big_tall_size",
"hc_men_apparel_bottom_size",
"hc_men_apparel_bottom_waist_size",
"hc_men_apparel_bottom_width",
"hc_men_apparel_button_up_shirt_size",
"hc_men_apparel_general_size",
"hc_men_apparel_inseam",
"hc_men_apparel_top_big_tall_size",
"hc_men_footwear_socks_size",
"hc_men_size",
"hc_men_width"
]

womens_facets = [
"hc_women_apparel_bottom_belt_size",
"hc_women_apparel_bottom_size",
"hc_women_apparel_bottom_waist_size",
"hc_women_apparel_bottom_width",
"hc_women_apparel_general_size",
"hc_women_apparel_inseam",
"hc_women_apparel_top_size",
"hc_women_footwear_socks_size",
"hc_women_size",
"hc_women_width"
]

universal_facets = [
    "size",
    "colorFacet",
    "gender"
]
    
config = ConfigParser.SafeConfigParser()
config.read("gangnam.config")
host = config.get("zappos", "API-host")
key = config.get("zappos", "API-key")

if __name__ == '__main__':
    CGIHandler().run(bottle.default_app())
