#! /usr/bin/env python
# -*- coding: utf-8 -*-
# To get http connection code for URL
import os
import socket
import urllib2

# Get http status code and handle exceptions for testurl array 
testurl=["https://localhost:8080", "http://localhost:5050"]
for url in testurl:
    try:
        print 'Testing URL' + str(url)
        connection = urllib2.urlopen(url)
        print "Connection Code for nginx sample site:%d" %connection.getcode()
        connection.close()
    except urllib2.HTTPError, e:
        print "Exception Instance for nginx sample site:%d" %e.getcode()