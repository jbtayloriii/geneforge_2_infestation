import flask

app = flask.Flask(__name__)


@app.route('/')
def landing_page():
    return "test"
#   return flask.render_template('index.html')
