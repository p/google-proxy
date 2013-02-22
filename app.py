import flask
import munge

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/search')
def index():
    query = flask.request.args
    return munge.index(query)

if __name__ == '__main__':
    app.run(port=8007)
