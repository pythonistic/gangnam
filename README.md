Gangnam
=======

Find your _Gangnam Style_ by using Zappos' search tools to find similar clothing, shoes, and accessories in your size.

Development Site
----------------
http://www.pythonistic.com/gangnam

Requirements
------------
This is written in Python 2.6 using [bottle](http://bottlepy.org).  Instructions for setting up an environment on
Dreamhost that can run the application are available at
[this blog post](http://www.mischiefblog.com/2012/08/18/a-simple-fastcgi-bottle-py-python-web-application-for-dreamhost/).

You will need to obtain a Zappos API key from (http://developers.zappos.com).  After you have your API key, you need to
set up a *gangnam.config* file with the following entries (replace the *x* characters with the values returned by Zappos):

    [zappos]
    appId: xxxx
    API-key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    API-host: http://api.zappos.com
