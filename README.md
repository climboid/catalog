# Catalog Project

Basic CRUD in python with OAUTH using Google, SQLAlchemy for the ORM (SQLite), and Flask for the Python Framework.

## Files
application.py - CRUD operations and logic
client_secrets.json - used for OAUTH with Google
database_setup.py - creates the database tables
lotsofcatalogitems.py - populates the database
static/styles.css - stylesheet for the application
templates/*.html - all the html templates

## Libraries
[SQLAlchemy](http://docs.sqlalchemy.org/en/rel_1_0/intro.html#installation-guide) - ORM used to interact with the DB. 
[Flask](http://flask.pocoo.org/docs/0.10/installation/) - Python microframework used to create REST API
[Twitter Bootstrap](http://getbootstrap.com/) - CSS Framework used for grid and html elements.
[Jquery-2.1.4](https://jquery.com/) - JavaScript library to ease cross browser compliance. 

## Modules
From Flask:
* render_template - Self explanatory
* request - allows AJAX calls
* redirect - redirects to a given method URL
* jsonify - converts to JSON format
* url_for - determines the url for a given method
* flash - allows message popups in app
* session as login_session - user session for the app [examples](http://flask.pocoo.org/snippets/category/sessions/)

### From SQLAlchemy:
* create_engine : Starting point of SQLAlchemy application [link](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html)
* sessionmaker : The orm.mapper() function and declarative extensions are the primary configurational interface for the ORM [link](http://docs.sqlalchemy.org/en/rel_1_0/orm/session.html)

### From database_setup:
* Base - Construct a base class for declarative class definitions. [link](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html)
* Category - Category class that creates the category table
* CategoryItem - CategoryItem class that creates the category_item table

### From Python:
* random - This module implements pseudo-random number generators for various distributions. [link](https://docs.python.org/2/library/random.html)
* string - The string module contains a number of useful constants and classes, as well as some deprecated legacy functions that are also available as methods on strings. [link](https://docs.python.org/2/library/string.html)
* httplib2 - A comprehensive HTTP client library [link](https://pypi.python.org/pypi/httplib2)
* json - JSON encoder and decoder [link](https://docs.python.org/2/library/json.html)
* make_response - Allows to set headers in a response [link](http://nullege.com/codes/search/flask.make_response)
* requests - Simple HTTP requests in a more user friendly format [link](http://docs.python-requests.org/en/latest/)

### From oauth2client.client:
* flow_from_clientsecrets - The oauth2client.client.flow_from_clientsecrets() method creates a Flow object from a client_secrets.json file. This JSON formatted file stores your client ID, client secret, and other OAuth 2.0 parameters. [link](https://developers.google.com/api-client-library/python/guide/aaa_oauth#flow_from_clientsecrets) 
* FlowExchangeError - Error trying to exchange an authorization grant for an access token. [link](https://google-api-python-client.googlecode.com/hg/docs/epy/oauth2client.client.FlowExchangeError-class.html)

## Instalation

To run this catalog project you will need python 2.7.9. 
To install python go to [this link](https://www.python.org/downloads/)

Depending on your setup you might need [SQLalchemy](http://docs.sqlalchemy.org/en/rel_1_0/intro.html#installation-guide) and [Flask](http://flask.pocoo.org/docs/0.10/installation/). Follow their links and installation guidelines accordingly.

## Running the application

Open your terminal & cd to this repo. Then type in the following commands:

1. ``` python database_setup.py ``` to create the database

2. ``` python lotsofcatalogitems.py ``` to populate the database

3. ``` python application.py ``` to launch the app. Navigate to localhost:5000 in your browser.





