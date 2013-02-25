import daemon
import bottle
import bapp

with daemon.DaemonContext():
    bottle.run(app=bapp.app, port=8008, server='flup')
