import flask
import urllib
import re
import cgi
import xml.sax.saxutils
import curlfe

app = flask.Flask(__name__)
#app.debug = True

def replace(match):
    url = match.group(1)
    url = xml.sax.saxutils.unescape(url)
    url = url[:url.find('&')]
    #url = url[:url.find('&amp;')]
    url = urllib.unquote(url)
    #print url
    url = xml.sax.saxutils.quoteattr(url)
    return 'href=%s' % url

@app.route('/')
@app.route('/search')
def index():
    args = {}
    for key in ['q', 'start']:
        value = flask.request.args.get(key)
        if value is not None:
            args[key] = value
    query = urllib.urlencode(args)
    if query:
        url = 'http://www.google.com/search?%s' % query
    else:
        url = 'http://www.google.com/'
    
    fe = curlfe.CurlFe()
    # http://curl.haxx.se/mail/curlpython-2007-07/0001.html
    # curl insists on a str, not unicode, on python 2
    url = url.encode('utf8')
    content = fe.fetch(url)
    content = re.sub(r'<script[^>]*>.*?</script>', '', content)
    content = re.sub(r'href="/url\?q=([^"]+)"', replace, content)
    # this causes forms to submit to google, not good
    #content = content.replace(r'<head>', '<head><base href="http://www.google.com/">')
    content = re.sub(r'url\(/(?!/)', 'url(http://www.google.com/', content)
    return content

if __name__ == '__main__':
    app.run()
