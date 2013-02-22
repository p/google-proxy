import bottle
import munge

app = bottle.Bottle()

@app.route('/')
@app.route('/<p:path>')
def index(p=None):
    query = bottle.request.query
    return munge.index(query)

if __name__ == '__main__':
    bottle.run(app, reloader=True)
