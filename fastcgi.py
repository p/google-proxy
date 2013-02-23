import bottle
import bapp

bottle.run(app=bapp.app, server=bottle.FlupFCGIServer, bindAddress=('localhost', 8008))
