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
@app.route('/category/<int:category_id>/items')
def showCategoryItems(category_id):
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(CategoryItem).filter_by(category_id=category_id).all()
	return render_template('category-items.html', items=items, categories=categories, category=category)

#
# Show a description of a category item
# TODO finish getting the URL just right
@app.route('/category/<int:category_id>/item/<int:item_id>')
def categoryItem(category_id, item_id):
	item = session.query(CategoryItem).filter_by(id = item_id).one()
	return render_template('category-item.html', item = item)


#
# Edit the category item
#
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    category= session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    print 'request.method', request.method
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category.name = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('intropage'))
    else:

        return render_template(
            'editcategory-item.html', item = editedItem, category = category)

#
# Delete category item
#
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', 
    methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(
            url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template(
            'deletecategory-item.html', item=itemToDelete, category = category)
    # return 'This page will be for deleting restaurant %s' % restaurant_id



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
