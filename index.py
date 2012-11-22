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
    host = config.get("zappos", "API-host")
    key = config.get("zappos", "API-key")
    url = host + "/Search/term/%s?key=%s" % (quote_plus(keyword), key)
    try:
        response = urllib2.urlopen(url)
        out = ""
        for line in response:
            out += line
        return "<pre>" + str(out) + "</pre>"
    except URLError as e:
        return "<font color=\"red\">Error: %s</font>" % (str(e))
    
config = ConfigParser.SafeConfigParser()
config.read("gangnam.config")

if __name__ == '__main__':
    CGIHandler().run(bottle.default_app())
