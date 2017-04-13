from functools import wraps
from flask import Blueprint, render_template, request, url_for, redirect
from flask import abort, jsonify, flash, escape
from flask import session as login_session
# from jinja2 import TemplateNotFound

import helpers
import pdb
import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User

private_page = Blueprint('private_page', __name__,
                        template_folder='templates')


# Decorator to check that a user is logged in before these pages can be
# accessed
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            flash("Please sign in first before accessing this page.")
            return redirect(url_for('loginSite'))
        return f(*args, **kwargs)

    return decorated_function


# Adds a new item to the catalog
@private_page.route('/catalog/item/add',
    methods=['POST', 'GET'])
@login_required
def newItem():
    if request.method == 'GET':
        return render_template('newitem.html')

    if request.method == 'POST':
        # The name of the item is required, at the minimum
        if len(request.form['name']) == 0:
            flash("The name of the item is mandatory!")
            return render_template('newitem.html',
                name=request.form['name'],
                price=request.form['price'],
                category=request.form['category'],
                description=request.form['description'])

        # Retrieves the user
        user_id = login_session['user_id']
        user = session.query(User).filter_by(id=int(user_id)).one()

        # Creates the record and saves it to the database
        new_item = CatalogItem(name=request.form['name'],
            price=request.form['price'],
            category=request.form['category'],
            description=request.form['description'],
            user=user)
        session.add(new_item)
        session.commit()

        # Retrieves the id of the added record for page redirect
        item = dbfunctions.getDescending(CatalogItem, CatalogItem.dt_added, 1)
        item = item[0]
        flash("New item added!")

        return redirect(url_for('public_page.viewCatalogItem',
            category=item.category,
            item_id=item.id))


# Edits the catalog item record
@private_page.route('/catalog/item/<int:item_id>/edit',
    methods=['POST', 'GET'])
@login_required
def editItem(item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()

    # Redirects back to the main landing page if the record is not found
    if not item:
        flash("Invalid item. \
            Please check that you have selected a valid item.")
        return redirect(url_for('public_page.itemList'))

    if request.method == 'GET':
        return render_template('edititem.html', item=item)

    if request.method == 'POST':
        user_id = login_session['user_id']

        # Checks that the item belongs to the rightful user
        if user_id == item.user_id:
            item.name = request.form['name']
            item.price = request.form['price']
            item.category = request.form['category']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            flash("Item saved successfully!")
        else:
            flash("You are not authorized to edit this item!")
            return redirect(url_for('public_page.viewCatalogItem',
                category=item.category,
                item_id=item.id))

        return redirect(url_for('public_page.viewCatalogItem',
            category=item.category,
            item_id=item.id))


# Deletes a catalog item
@private_page.route('/catalog/item/<int:item_id>/delete',
    methods=['POST', 'GET'])
@login_required
def deleteItem(item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()

    # Redirects back to the main landing page if the record is not found
    if not item:
        flash("Invalid item. \
            Please check that you have selected a valid item.")
        return redirect(url_for('public_page.itemList'))

    if request.method == 'GET':
        return render_template('deleteitem.html', item=item)

    if request.method == 'POST':
        user_id = login_session['user_id']

        # Checks that the user is the rightful owner of the item
        if user_id == item.user.id:
            session.delete(item)
            session.commit()
            flash("Item deleted!")
        else:
            flash("You are not authorized to delete this item!")
            return redirect(url_for('public_page.viewCatalogItem',
                category=item.category,
                item_id=item.id))

        return redirect(url_for('public_page.itemList'))
