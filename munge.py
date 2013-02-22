import urllib
import re
import cgi
import xml.sax.saxutils
import webracer.agent

def replace(match):
    url = match.group(1)
    url = xml.sax.saxutils.unescape(url)
    url = url[:url.find('&')]
    #url = url[:url.find('&amp;')]
    url = urllib.unquote(url)
    #print url
    url = xml.sax.saxutils.quoteattr(url)
    return 'href=%s' % url

def index(query_args):
    args = {}
    for key in ['q', 'start']:
        value = query_args.get(key)
        if value is not None:
            args[key] = value
    query = urllib.urlencode(args)
    if query:
        url = 'http://www.google.com/search?%s' % query
    else:
        url = 'http://www.google.com/'
    
    ua = webracer.agent.Agent(use_cookie_jar=False)
    # http://curl.haxx.se/mail/curlpython-2007-07/0001.html
    # curl insists on a str, not unicode, on python 2
    #url = url.encode('utf8')
    response = ua.get(url)
    content = response.body
    content = re.sub(r'<script[^>]*>.*?</script>', '', content)
    content = re.sub(r'href="/url\?q=([^"]+)"', replace, content)
    content = re.sub(r'href="/interstitial\?url=([^"]+)"', replace, content)
    # this causes forms to submit to google, not good
    #content = content.replace(r'<head>', '<head><base href="http://www.google.com/">')
    content = re.sub(r'url\(/(?!/)', 'url(http://www.google.com/', content)
    return content
