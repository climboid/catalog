from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem
from flask import session as login_session

import random
import string
import httplib2
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///cataloglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

#
# Connect OAUTH with Google
#
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print 'error', result.get('error')
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    print 'answer', answer
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += ' 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#
# Logout Google OAUTH
#
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#
# Landig page
#
@app.route('/')
def intropage():
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    credentials = login_session.get('credentials')
    if credentials is None:
        return render_template('category.html', categories = categories, 
            items = items)
    else:
        return render_template('category.html', categories = categories, 
            items = items, login_session = login_session)


#
# Show all items that belong to a category
#
@app.route('/category/<int:category_id>/items')
def showCategoryItems(category_id):
    credentials = login_session.get('credentials')
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category_id).all()

    if credentials is None:
        return render_template('category-items.html', items=items, 
            categories=categories, category=category)
    else:
        return render_template('category-items.html', items=items, 
            categories=categories, category=category, 
            login_session = login_session)

#
# Show all items that belong to a category in JSON format
#
@app.route('/category/<int:category_id>/items/JSON')
def restaurantMenuJSON(category_id):
    items = session.query(CategoryItem).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])

#
# Show a description of a category item
# 
@app.route('/category/<int:category_id>/item/<int:item_id>')
def categoryItem(category_id, item_id):
    credentials = login_session.get('credentials')
    item = session.query(CategoryItem).filter_by(id = item_id).one()
    category= session.query(Category).filter_by(id=category_id).one()
    if credentials is None:
        return render_template('category-item.html', item = item, 
            category = category)
    else:
        return render_template('category-item.html', item = item, 
            category = category, login_session = login_session)


#
# Edit the category item
#
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')
    categories = session.query(Category).all()
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one();

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('intropage'))
    else:

        return render_template(
            'editcategory-item.html', item = editedItem, 
            categories = categories, category = category, login_session = login_session)

#
# Add a category item
#
@app.route('/category/add', methods=['GET', 'POST'])
def addCategoryItem():
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')

    category_list = session.query(Category).all()

    if request.method == 'POST':
        
        selectedCategory = name=request.form['category']
        print 'selectedCategory', selectedCategory
        category= session.query(Category).filter_by(id=selectedCategory).one()

        newItem = CategoryItem(name=request.form['name'],
                description=request.form['description'],
                category = category)

        session.add(newItem)
        session.commit()
        return redirect(url_for('intropage'))
    else:
        return render_template('addcategory-item.html', 
            category_list = category_list, login_session = login_session)

#
# Delete category item
#
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', 
    methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect('/')
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(
            url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template(
            'deletecategory-item.html', item=itemToDelete, 
            category = category, login_session = login_session)
    # return 'This page will be for deleting restaurant %s' % restaurant_id



if __name__ == '__main__':
    app.secret_key = 'ArhTQbToCDUEcfmcpitHS_1T'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
