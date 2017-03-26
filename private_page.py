from functools import wraps
from flask import Blueprint, render_template, abort, jsonify, request, flash, url_for, redirect, escape
from flask import session as login_session
from jinja2 import TemplateNotFound

import helpers
import pdb
import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User

private_page = Blueprint('private_page', __name__,
                        template_folder='templates')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in login_session:
            flash("Please sign in first before accessing this page.")
            return redirect(url_for('loginSite'))
        return f(*args, **kwargs)

    return decorated_function


# Adds a new menu item to a restaurant
@private_page.route('/catalog/item/add',
    methods = ['POST', 'GET'])
@login_required
def newItem():
    if request.method == 'GET':
        return render_template('newitem.html')

    if request.method == 'POST':
        # if 'userid'  not in login_session:
        #     flash("Please log in first to add an item.")
        #     return redirect(url_for('loginSite'))

        if len(request.form['name']) == 0:
            flash("The name of the item is mandatory!")
            return render_template('newitem.html',
                name = request.form['name'],
                price = request.form['price'],
                category = request.form['category'],
                description = request.form['description'])

        user_id = login_session['userid']
        user = session.query(User).filter_by(id = int(user_id)).one()

        new_item = CatalogItem(name = request.form['name'],
            price  = request.form['price'],
            category  = request.form['category'],
            description = request.form['description'],
            user = user)
        session.add(new_item)
        session.commit()

        item = dbfunctions.getDescending(CatalogItem, CatalogItem.dt_added, 1)
        item = item[0]
        flash("New item added!")

        return redirect(url_for('public_page.viewCatalogItem',
            category = item.category,
            item_id = item.id))


# Edits a single menu item of a restaurant
@private_page.route('/catalog/item/<int:item_id>/edit',
    methods = ['POST', 'GET'])
@login_required
def editItem(item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if not item:
        flash("Invalid item. \
            Please check that you have selected a valid item.")
        return redirect(url_for('public_page.viewCatalogItem',
            item_id = item_id))

    if request.method == 'GET':
        return render_template('edititem.html', item = item)

    if request.method == 'POST':
        # if 'userid'  not in login_session:
        #     flash("Please log in first to edit the item.")
        #     return redirect(url_for('public_page.loginSite'))

        user_id = login_session['userid']

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
                category = item.category,
                item_id = item.id))

        return redirect(url_for('public_page.viewCatalogItem',
            category = item.category,
            item_id = item.id))


# Deletes a menu item
@private_page.route('/catalog/item/<int:item_id>/delete',
    methods = ['POST', 'GET'])
@login_required
def deleteItem(item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if not item:
        flash("Invalid item. \
            Please check that you have selected a valid item.")
        return redirect(url_for('public_page.viewCatalogItem',
            item_id = item_id))

    if request.method == 'GET':
        return render_template('deleteitem.html', item = item)

    if request.method == 'POST':
        # if 'userid'  not in login_session:
        #     flash("Please log in first to delete the item.")
        #     return redirect(url_for('loginSite'))

        user_id = login_session['userid']

        if user_id == item.user.id:
            session.delete(item)
            session.commit()
            flash("Item deleted!")
        else:
            flash("You are not authorized to delete this item!")
            return redirect(url_for('public_page.viewCatalogItem',
                category = item.category,
                item_id = item.id))

        return redirect(url_for('public_page.itemList'))