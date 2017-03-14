from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User

public_page = Blueprint('public_page', __name__,
                        template_folder='templates')


@public_page.route('/', methods = ['GET'])
def itemList():
    items = session.query(CatalogItem).order_by(CatalogItem.dt_modded).limit(5)
    categories = dbfunctions.getUnique(CatalogItem.category)
    cat_name = list(k[0] for k in categories)
    return render_template('index.html', items = items, categories = cat_name)