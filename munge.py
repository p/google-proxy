import sys, urlparse
import socket
import urllib
import re
import cgi
import xml.sax.saxutils
import webracer.agent

class Redirect(StandardError):
    pass

class OpenDnsDetected(StandardError):
    pass

opendns_ips = ['208.67.222.222', '208.67.220.220']

def check_opendns():
    with open('/etc/resolv.conf') as f:
        conf = f.read()
    words = re.split(r'\s+', conf)
    for ip in opendns_ips:
        if ip in words:
            return True
    return False

def replace(match):
    url = match.group(1)
    url = xml.sax.saxutils.unescape(url)
    url = url[:url.find('&')]
    #url = url[:url.find('&amp;')]
    url = urllib.unquote(url)
    #print url
    url = xml.sax.saxutils.quoteattr(url)
    return 'href=%s' % url

def replace_adurl(match):
    query = match.group(1)
    qs = urlparse.parse_qs(query)
    return 'href=%s' % cgi.escape(qs['adurl'][0])

def index(query_args):
    # workaround for http://my.opera.com/community/forums/topic.dml?id=486461
    if 'q' in query_args and 'start' not in query_args and \
        'sourceid' in query_args and query_args['sourceid'] == 'opera':
            host = query_args['q']
            if re.match(r'[a-zA-Z0-9\-]+$', host):
                if check_opendns():
                    return 'opendns detected, please fix'
                exc = None
                try:
                    hostname = socket.gethostbyname(host)
                    if hostname:
                        exc = Redirect('http://%s' % host)
                except:
                    #print sys.exc_info()
                    pass
                if exc is not None:
                    raise exc
    
    args = {}
    for key in ['q', 'start', 'spell']:
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
    content = re.compile(r'<script[^>]*>.*?</script>', re.S).sub('', content)
    content = re.sub(r'href="/url\?q=([^"]+)"', replace, content)
    content = re.sub(r'href="/aclk\?([^"]+)"', replace_adurl, content)
    content = re.sub(r'href="/interstitial\?url=([^"]+)"', replace, content)
    # this causes forms to submit to google, not good
    #content = content.replace(r'<head>', '<head><base href="http://www.google.com/">')
    content = re.sub(r'url\(/(?!/)', 'url(http://www.google.com/', content)
    return content
