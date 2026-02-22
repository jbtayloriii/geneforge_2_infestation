"""Main entrypoint for the geneforge site."""
import csv

import objects
import data_loader

import flask



app = flask.Flask(__name__)

_DATA = data_loader.DataLoader()


@app.route('/')
def landing_page():
    return flask.render_template("index.html")

@app.route('/zones')
def zones():
    return "TODO"

@app.route('/items')
def items():
    return flask.render_template(
        "items.html",
        item_variety_by_id=_DATA.item_varieties_by_id,
        item_templates_by_variety_id=_DATA.item_templates_by_variety_id
    )

@app.route('/item_template/<item_id>')
def item_template(item_id):

    int_id = int(item_id)
    template = _DATA.item_templates_by_id[int_id] if int_id in _DATA.item_templates_by_id else None
    return flask.render_template("item_template.html", template=template)

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
