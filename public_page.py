from flask import Blueprint, render_template, abort, jsonify, url_for, redirect
# from jinja2 import TemplateNotFound

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem

public_page = Blueprint('public_page', __name__,
                        template_folder='templates')


# Main landing page. Displays the list of restaurants
# By categories and by last modified
@public_page.route('/', methods=['GET'])
def itemList():
    items = session.query(CatalogItem).order_by(CatalogItem.dt_modded).limit(5)
    categories = dbfunctions.getUnique(CatalogItem.category)
    cat_name = list(k[0] for k in categories)
    return render_template('index.html', items=items, categories=cat_name)


# API request endpoint for the full list of available catalog items
@public_page.route('/catalog/JSON')
def catalogitemJSON():
    catalogitem = session.query(CatalogItem).all()
    return jsonify(CatalogItem=[i.serialize for i in catalogitem])


# API request endpoint for single items
@public_page.route('/catalog/<string:category>/items/<int:item_id>/JSON')
def singleitemJSON(category, item_id):
    catalogitem = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(CatalogItem=[catalogitem.serialize])


# Displays all items of a category
@public_page.route('/catalog/<string:category>/items', methods=['GET'])
@public_page.route('/catalog/<string:category>', methods=['GET'])
def viewCategory(category):
    items = session.query(CatalogItem).filter_by(category=category).all()
    categories = dbfunctions.getUnique(CatalogItem.category)
    cat_name = list(k[0] for k in categories)
    return render_template('categorylist.html',
        items=items,
        category=category,
        categories=cat_name)


# Displays the selected item
@public_page.route('/catalog/<string:category>/items/<int:item_id>',
    methods=['GET'])
def viewCatalogItem(category, item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return render_template('viewitem.html', item=item)
