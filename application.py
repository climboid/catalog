from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)

engine = create_engine('sqlite:///cataloglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#
# Landig page
#
@app.route('/')
def intropage():
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    return render_template('main.html', categories = categories, items = items)

#
# Show all items that belong to a category
#
@app.route('/catalog/<int:category_id>/items')
def showCategoryItems(category_id):
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(CategoryItem).filter_by(category_id=category_id).all()
	return render_template('category-items.html', items=items, categories=categories, category=category)

#
# Show a description of a category item
# TODO finish getting the URL just right
@app.route('/catalog/<string:category_name>/<int:item_id>')
def categoryItem(category_name, item_id):
	item = session.query(CategoryItem).filter_by(id = item_id).one()
	return render_template('category-item.html', item = item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
