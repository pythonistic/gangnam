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
    sex = request.forms.sex
    request_facets = {}
    if sex == 'M':
        for facet in mens_facets:
            if facet in request.forms:
                request_facets[facet] = request.forms[facet]
    elif sex == 'F':
        for facet in womens_facets:
            if facet in request.forms:
                request_facets[facet] = request.forms[facet]
    for facet in universal_facets:
        if facet in request.forms:
                request_facets[facet] = request.forms[facet]
    
    url = host + "/Search/term/%s?filters=%s&key=%s" % (quote_plus(keyword), build_facets(request_facets), key)
    try:
        response = urllib2.urlopen(url)
        out = ""
        for line in response:
            out += line
        return "<b>REQUEST</b><br/><pre>" + str(url) + "</pre><p/><b>RESPONSE</b><br/><pre>" + str(out) + "</pre>"
    except URLError as e:
        return "<font color=\"red\">Error: %s</font>" % (str(e))

def build_facets(request_facets):
    out = {}
    for facet in request_facets:
        if type(request_facets[facet] == str):
            out['"' + facet + '"'] = '["' + request_facets[facet] + '"]'
        elif type(request_facets[facet] == list):
            values = []
            for value in request_facets[facet]:
                values.append('"' + value + '"')
            out['"' + facet + '"'] = '[' + ",".join(values) + ']'
    
    return out
    
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
    "colorFacet"
]
    
config = ConfigParser.SafeConfigParser()
config.read("gangnam.config")
host = config.get("zappos", "API-host")
key = config.get("zappos", "API-key")

if __name__ == '__main__':
    CGIHandler().run(bottle.default_app())
