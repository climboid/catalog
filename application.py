from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)

engine = create_engine('sqlite:///cataloglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def restaurantsJSON():
    categories = session.query(Category).all()
    #categories = jsonify(categories=[r.serialize for r in categories])
    items = session.query(CategoryItem).all()
    #items = jsonify(items=[r.serialize for r in items])
    #return jsonify(categories=[r.serialize for r in categories], items=[r.serialize for r in items])
    return render_template('main.html', categories = categories, items = items)


# Show all restaurants
# @app.route('/')
# @app.route('/restaurant/')
# def showRestaurants():
#     restaurants = session.query(Restaurant).all()
#     # return "This page will show all my restaurants"
#     return render_template('restaurants.html', restaurants=restaurants)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
