#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Catalog Project server"""
from flask import Flask, render_template, json, jsonify, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User, DB_CONN_URI

# Flask app
app = Flask(__name__)

# Connect to database
engine = create_engine(DB_CONN_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
@app.route("/catalog")
def main():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.lastEditTime).limit(20).all()
    return render_template("main.html", categories=categories, items=items)


@app.route("/catalog.json")
def catalogJson():
    catalog = [c.serialize for c in session.query(Category).all()]
    return Response(response=json.dumps({'catalog': catalog}, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<category_name>.json")
def categoryJson(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    return Response(response=json.dumps(category.serialize, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<item_name>.json")
def itemJson(item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return Response(response=json.dumps(item.serialize, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<category_name>/")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    categories = session.query(Category).limit(10).all()
    category = session.query(Category).filter_by(name=category_name).one()
    return render_template("showCategory.html",
                           categories=categories,
                           category=category)


@app.route("/catalog/<category_name>/<item_name>")
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,
                                         category=category).one()
    return render_template("showItem.html", item=item)


@app.route("/catalog/add", methods=['GET', 'POST'])
@app.route("/catalog/<category_name>/add", methods=['GET', 'POST'])
def addItem(category_name=None):
    return render_template("addItem.html", category=category_name)


@app.route("/catalog/<item_name>/edit", methods=['GET', 'POST'])
def editItem(item_name):
    return render_template("editItem.html", item=item_name)


@app.route("/catalog/<item_name>/delete", methods=['GET', 'POST'])
def deleteItem(item_name):
    return render_template("deleteItem.html", item=item_name)


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0", 5000)
