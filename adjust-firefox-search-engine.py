#!/usr/bin/env python

# The search plugins live at:
# /usr/local/lib/firefox/searchplugins
#
# Source:
# http://hg.mozilla.org/mozilla-central/annotate/2876e73c9b6f/browser/locales/en-US/searchplugins/google.xml
#
# This is what we are killing:
# https://bugzilla.mozilla.org/show_bug.cgi?id=722352
# http://www.monperrus.net/martin/the+meaning+of+parameter+aq+in+google+queries+and+referer+fields
# https://bugzilla.mozilla.org/show_bug.cgi?id=359880
#
# Firefox caches search plugins into search.json under profile directory,
# that needs to be nuked after search plugins are edited.

import lxml.etree
import sys
import urlparse

def fix_url(url):
    parts = list(urlparse.urlparse(url))
    parts[0] = 'http'
    parts[1] = 'gs'
    url = urlparse.urlunparse(parts)
    return url

def adjust_in_place(path):
    with open(path) as f:
        xml = f.read()
    
    doc = lxml.etree.XML(xml)
    for element in doc.iter('{*}Url'):
        url = element.attrib['template']
        url = fix_url(url)
        element.attrib['template'] = url
    for element in doc.iter('{*}SearchForm'):
        element.text = fix_url(element.text)
    for element in doc.iter('{*}Param'):
        if element.attrib['name'] in ['channel', 'rls', 'aq']:
            element.getparent().remove(element)
    for element in doc.iter('{*}MozParam'):
        if element.attrib['name'] in ['client']:
            element.getparent().remove(element)
    
    xml = lxml.etree.tostring(doc)
    print xml

if len(sys.argv) > 1:
    adjust_in_place(sys.argv[1])
