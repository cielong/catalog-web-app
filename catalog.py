#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Catalog Project server"""
from flask import Flask, render_template, jsonify
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
    items = session.query(Item).order_by(Item.last_edit).limit(20).all()
    return render_template("main.html", categories=categories, items=items)


@app.route("/catalog.json")
def catalogJson():
    return jsonify(catalog=["catalog"])


@app.route("/catalog/<category_name>.json")
def categoryJson():
    return jsonify(category=['category'])


@app.route("/catalog/<item_name>.json")
def itemJson():
    return jsonify(item=['item'])


@app.route("/catalog/<category_name>/")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    return render_template("showCategory.html",
                           categories=["Snowboarding"],
                           category="category",
                           items=["snowboard"])


@app.route("/catalog/<category_name>/<item_name>")
def showItem(category_name, item_name):
    return render_template("showItemLoggedIn.html", category=category_name,
                           item=item_name)


@app.route("/catalog/add", methods=['GET', 'POST'])
@app.route("/catalog/<category_name>/add")
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
