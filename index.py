#!/bin/env python

from flask import Flask, make_response, render_template, request, Response

import configparser
import json
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import quote_plus

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return "OK"


@app.route('/hello/<name>')
def hello(name):
    return "Hello %s" % (name)


@app.route('/swiper')
def swiper():
    return render_template('swiper.html')


@app.route('/search/<keyword>')
def search(keyword):
    url = host + "/Search/term/%s?key=%s" % (quote_plus(keyword), key)
    results = json.dumps(query_api(url)['results'])
    response = Response(results, 200, mimetype="application/json")
    return response


@app.route('/search_rows/<keyword>')
def search_rows(keyword):
    print("entering search_rows")
    url = host + "/Search/term/%s?key=%s" % (quote_plus(keyword), key)
    results = query_api(url)['results']
    print("got %s results" % len(results))
    # build the result rows
    result_rows = []
    start_idx = 0
    while start_idx < len(results):
        start_idx = len(result_rows) * 6
        end_idx = start_idx + 6
        result_row = []
        for idx in range(start_idx, end_idx):
            if idx < len(results):
                result_row.append(results[idx])
            else:
                result_row.append(None)
        result_rows.append(result_row)
    print(result_rows)
    # render the page fragment
    return render_template('search_rows.html', result_rows=result_rows)

@app.route('/searchsize/<keyword>', methods=["POST"])
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
    results = query_api(url)
    return "<pre>" + str(results) + "</pre>"

def query_api(url):
    """
    Query the Zappos API and return the JSON object turned into a dict.
    :param url: the Zappos API URI.
    :return: the dict response.
    """
    print(url)
    try:
        response = urlopen(url)
        out = ""
        for line in response.readlines():
            out += bytes.decode(line)
        print(out)
        return json.loads(out)
    except URLError as e:
        return "<font color=\"red\">Error: %s</font>" % (str(e))


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
    
config = configparser.ConfigParser()
config.read("gangnam.config")
host = config.get("zappos", "API-host")
key = config.get("zappos", "API-key")

if __name__ == '__main__':
    app.run()