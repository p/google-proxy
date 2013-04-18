import bottle
import munge

app = bottle.Bottle()

@app.route('/')
@app.route('/<p:path>')
def index(p=None):
    query = bottle.request.query
    try:
        munge.index(query)
    except munge.Redirect as e:
        bottle.redirect(e.args[0])

if __name__ == '__main__':
    bottle.run(app, reloader=True, port=8007)
