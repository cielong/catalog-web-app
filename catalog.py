#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Catalog Project server"""
from flask import (
    Flask, render_template, json, Response, request, redirect,
    url_for
)

from flask_sslify import SSLify

# read command line arguments for setting flask app
from _flaskHelper import flaskrun

# Form formats
from forms import ItemInfoForm, ReferenceForm, RegistrationForm

# datebase connection
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from database_setup import (
    Base, Item, Category, User, Reference,
    user_with_item, DB_CONN_URI
)

# State
import random
import string
from flask import session as login_session

# OAuth2
import requests
import httplib2
from flask import make_response, flash
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError

# enviroment variable
import os
G_CLIENT_ID = os.environ['G_CLIENT_ID']
G_CLIENT_SECRET = os.environ['G_CLIENT_SECRET']

# Flask app
app = Flask(__name__)
sslify = SSLify(app)

# Connect to database
engine = create_engine(DB_CONN_URI, echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
Session = scoped_session(DBSession)
session = Session()


# For each request, rollback the transaction if error exists
@app.teardown_request
def session_clear(exception=None):
    """Clear session"""
    Session.remove()
    if exception and session.is_active:
        session.rollback()


# Page routes
@app.route("/")
@app.route("/catalog/")
def main():
    """Main page"""
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.lastEditTime.desc())
    items = items.limit(20).all()
    if 'username' in login_session:
        user = getUser(login_session['email'])
    else:
        user = None
    return render_template("main.html", categories=categories,
                           items=items, user=user)


@app.route("/catalog.json")
def catalogJson():
    """API get all catalog information in json database"""
    catalog = [c.serialize for c in session.query(Category).all()]
    return Response(response=json.dumps({'catalog': catalog}, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<category_name>.json")
def categoryJson(category_name):
    """API get a category information in json format"""
    category = session.query(Category).filter_by(name=category_name).one()
    return Response(response=json.dumps(category.serialize, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<category_name>/<item_name>.json")
def itemJson(category_name, item_name):
    """API get an item information in json formats"""
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item)
    item = item.filter(Item.categories.contains(category))
    item = item.filter_by(name=item_name).one()
    return Response(response=json.dumps(item.serialize, indent=2,
                                        ensure_ascii=False,
                                        separators=(',', ': ')),
                    status=200, mimetype='application/json')


@app.route("/catalog/<category_name>/")
@app.route("/catalog/<category_name>/items")
def showCategory(category_name):
    """Retrieve a category and its items in database
       Assume a category is uniquely defined by its name

    Args:
        category_name: the name of the category
    """

    categories = session.query(Category).limit(10).all()
    category = session.query(Category).filter_by(name=category_name).one()
    if 'username' in login_session:
        user = getUser(login_session['email'])
        return render_template("showCategoryLoggedIn.html",
                               categories=categories,
                               category=category,
                               user=user)
    else:
        return render_template("showCategory.html",
                               categories=categories,
                               category=category)


@app.route("/catalog/<category_name>/<item_name>")
def showItem(category_name, item_name):
    """Retrieve an item in database
       Assume an item is uniquely defined by its name

    Args:
        category_name: the name of the category
        item_name: the name of the item
    """
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item)
    item = item.filter(Item.categories.contains(category))
    item = item.filter_by(name=item_name).one()
    if 'username' in login_session:
        user = getUser(login_session['email'])
        return render_template("showItemLoggedIn.html",
                               item=item, user=user)
    else:
        return render_template("showItem.html", item=item)


@app.route("/catalog/add", methods=['GET', 'POST'])
@app.route("/catalog/<category_name>/add", methods=['GET', 'POST'])
def addItem(category_name=None):
    """Add new Item

    Args:
        category_name: the name of the category which direct to this page
    """
    if 'username' not in login_session:
        return redirect('/login')
    user = getUser(login_session['email'])
    if not user:
        return make_response(json.dumps("Email Address doesn't exists!"
                                        " Please sign in with another"
                                        " email address"), 401)
    form = ItemInfoForm(request.form)
    if request.method == 'POST' and form.validate():
        item = Item(name=form.name.data, description=form.description.data)
        # Add reference
        for reference in form.references:
            reference = Reference(rtext=reference.form.Text.data,
                                  rlink=reference.form.Link.data)
            reference.item = item
            item.refers.append(reference)
            session.add(reference)
        # Add category
        for category in form.categories:
            try:
                c = session.query(Category).filter_by(name=category.data).one()
            except NoResultFound:
                c = Category(name=category.data)
                session.add(c)
            c.items.append(item)
        # Add user
        uwi = user_with_item()
        uwi.item = item
        uwi.user = user
        user.items.append(uwi)
        session.commit()
        return redirect(url_for('showItem',
                                category_name=item.categories[0].name,
                                item_name=item.name))
    else:
        categories = session.query(Category).all()
        if category_name:
            category = session.query(Category).\
                filter_by(name=category_name).one()
        else:
            category = None
        return render_template("addItem.html", form=form,
                               category=category, categories=categories,
                               user=user)


@app.route("/catalog/<item_name>/edit", methods=['GET', 'POST'])
def editItem(item_name):
    """Edit/Update Item in their database
       Assume an item is uniquely defined by its name

    Args:
        item_name: the name of the item
    """
    if 'username' not in login_session:
        redirect('/login')
    user = getUser(login_session['email'])
    if not user:
        return make_response(json.dumps("Email Address doesn't exists!"
                                        " Please sign in with another"
                                        " email address"), 401)
    form = ItemInfoForm(request.form)
    item = session.query(Item).filter_by(name=item_name).one()
    if request.method == 'POST' and form.validate():
        item.name = form.name.data
        item.description = form.description.data
        # Add categories
        for c in form.categories:
            try:
                c = session.query(Category).filter_by(name=c.data).one()
            except NoResultFound:
                c = Category(name=c.data)
                session.add(c)
            c.items.append(item)

        try:
            uwi = session.query(user_with_item).filter_by(uid=user.id,
                                                          iid=item.id).one()
        except NoResultFound:
            uwi = user_with_item()
            uwi.item = item
            uwi.user = user

        # Add references
        for r in form.references:
            try:
                r = session.query(Reference).\
                    filter_by(iid=item.id).\
                    filter(or_(Reference.rtext == r.form.Text.data,
                               Reference.rlink == r.form.Link.data)).one()
            except NoResultFound:
                r = Reference(rtext=r.form.Text.data,
                              rlink=r.form.Link.data)
                item.refers.append(r)
                r.item = item
                session.add(r)

        # Add User
        user.items.append(uwi)
        session.add(uwi)
        session.commit()
        print("succeed!")
        item = session.query(Item).filter_by(name=item.name).one()
        return redirect(url_for('showItem',
                                category_name=item.categories[0].name,
                                item_name=item.name))
    else:
        # Add pre-filled contents (Current data) to their form
        categories = session.query(Category).all()
        form.description.data = item.description
        form.categories.pop_entry()
        for c in item.categories:
            form.categories.append_entry(c)
        form.references.pop_entry()
        for r in item.refers:
            rform = ReferenceForm()
            rform.Text = r.rtext
            rform.Link = r.rlink
            form.references.append_entry(rform)
        return render_template("editItem.html", form=form,
                               categories=categories,
                               item=item, user=user)


@app.route("/catalog/<item_name>/delete", methods=['GET', 'POST'])
def deleteItem(item_name):
    """Delete an item in database.
       Assume an item is uniquely defined by its name

    Args:
        item_name: the name of the item, embeded in the uri
    """
    if 'username' not in login_session:
        redirect('/login')
    user = getUser(login_session['email'])
    if not user:
        return make_response(json.dumps("Email Address doesn't exists!"
                                        " Please sign in with another"
                                        " email address"), 401)
    item = session.query(Item).filter_by(name=item_name).first()
    if request.method == 'POST':
        refers = session.query(Reference).filter_by(iid=item.id).all()
        for refer in refers:
            session.delete(refer)
        uwis = session.query(user_with_item).filter_by(iid=item.id).all()
        for relationship in uwis:
            session.delete(relationship)
        categories = session.query(Category).\
            filter(Category.items.contains(item)).all()
        for category in categories:
            category.items.remove(item)
        session.delete(item)
        flash('%s successfully deleted' % item.name)
        session.commit()
        return redirect(url_for('showCategory',
                                category_name=categories[0].name))
    else:
        return render_template("deleteItem.html", item=item, user=user)


@app.route("/signup", methods=['GET', 'POST'])
def showSignup():
    """ Register page """
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = getUser(email)
        if user:
            return make_response(json.dumps("Email Address has been"
                                            " registered. Please SignIn"), 401)
        username = form.username.data
        password = form.password.data
        newUser = User(email=email, username=username)
        newUser.hash_password(password)
        session.add(newUser)
        session.commit()
        return redirect('/login')
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=['POST', 'GET'])
def showLogin():
    """ Login page """
    state = ''.join([random.choice(string.ascii_letters+string.digits)
                     for _ in range(32)])
    login_session['state'] = state
    if request.method == 'GET':
        return render_template("login.html", STATE=state,
                               googleClientId=G_CLIENT_ID)
    else:
        email = request.form['email']
        user = getUser(email)
        if not user:
            return make_response(json.dumps("User not exists."
                                            " Did you forget your password?"),
                                 401)
        if not user.validate_password(request.form['password']):
            return make_response(json.dumps("Email/password incorrect."
                                            " Please try again."), 401)
        login_session['email'] = email
        login_session['username'] = user.username
        login_session['photo'] = user.photo
        return redirect('/catalog')


@app.route('/logout')
def logout():
    """Logout page"""
    access_token = login_session.get('access_token')
    if access_token:
        # If using Google Login
        return gdisconnect()
    else:
        # If user local user system
        try:
            del login_session['email']
            del login_session['username']
            del login_session['photo']
            flash('Successfully logged out. See you again.')
        except Exception:
            pass
        return redirect('/catalog')


@app.route("/gconnect", methods=['POST'])
def gconnect():
    """Connect to a google account using OAuth2"""
    # Check state token random generated in login
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    # OAuth flow (Get Access Token)
    try:
        oauth_flow = OAuth2WebServerFlow(client_id=G_CLIENT_ID,
                                         client_secret=G_CLIENT_SECRET,
                                         scope='',
                                         redirect_uri='postmessage')
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade their'
                                            'authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check token
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/"
           "tokeninfo?access_token=%s" % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match"
                                            " given User ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != G_CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does"
                                            " note match apps"), 401)
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is alredy'
                                            ' connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get User Info
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['photo'] = data['picture']
    login_session['email'] = data['email']

    # Login User
    user = getUser(login_session['email'])
    if not user:
        user = createUser(login_session)
    if user.photo is None:
        user.photo = login_session['photo']
        session.add(user)
        session.commit()
    flash("you are now logged in as %s" % user.username)
    return "Welcome %s" % user.username


def gdisconnect():
    """Disconnect google login accounts"""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user note connected!'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['photo']
        flash("Successfully log out!")
        return redirect("/catalog")
    else:
        try:
            login_session.clear()
        except Exception:
            pass
        response = make_response(json.dumps("Failed to revoke token "
                                            "for given user!"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


def getUser(email):
    """Get user from local database using unique email address"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except NoResultFound:
        return None


def createUser(login_session):
    """Create a user using information in login session"""
    newUser = User(email=login_session['email'],
                   username=login_session['username'],
                   photo=login_session['photo'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user


if __name__ == "__main__":
    try:
        app.secret_key = os.urandom(16)
        app.config['SESSION_TYPE'] = 'filesystem'
        flaskrun(app)
    except KeyboardInterrupt:
        login_session.clear()
