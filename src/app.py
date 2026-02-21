import flask

app = flask.Flask(__name__)


@app.route('/')
def landing_page():
    return flask.render_template("index.html")

@app.route('/zones')
def zones():
    return "TODO"

@app.route('/items')
def items():
    return "TODO"

@app.route('/canisters')
def canisters():
    return "TODO"

@app.route('/quests')
def quests():
    return "TODO"

@app.route('/skills')
def skills():
    return "TODO"

@app.route('/reputation')
def reputation():
    return "TODO"

@app.route('/special_items')
def special_items():
    return "TODO"

@app.route('/shops')
def shops():
    return "TODO"

@app.route('/crafting')
def crafting():
    return "TODO"
