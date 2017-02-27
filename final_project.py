# Standard Library
import pdb

# Third party modules
from flask import Flask
from flask import request, render_template, redirect, url_for, flash, jsonify
from flask import session as login_session, escape
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

# Local custom modules
import authenticate
from database_setup import Base, CatalogItem, User


app = Flask(__name__)

# Starts the database
engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# API request endpoint for the full list of available restaurants
@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurant])


# API request endpoint the menu of the specified restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()

    return jsonify(MenuItems=[i.serialize for i in items])


# Main landing page. Displays the list of restaurants
# By categories and by last modified
@app.route('/', methods = ['GET'])
def itemList():
    items = session.query(CatalogItem).order_by(CatalogItem.dt_modded).limit(5)
    categories = session.query(CatalogItem.category).distinct(CatalogItem.category).all()
    cat_name = list(k[0] for k in categories)
    return render_template('index.html', items = items, categories = cat_name)


# Displays all items of a category
@app.route('/catalog/<string:category>/items', methods = ['GET'])
@app.route('/catalog/<string:category>', methods = ['GET'])
def viewCategory(category):
    items = session.query(CatalogItem).filter_by(category = category).all()
    categories = session.query(CatalogItem.category).distinct(CatalogItem.category).all()
    cat_name = list(k[0] for k in categories)
    return render_template('categorylist.html', items = items, category = category, categories = cat_name)


# Displays the selected item
@app.route('/catalog/<string:category>/items/<int:item_id>', methods = ['GET'])
def viewCatalogItem(category, item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()
    return render_template('viewitem.html', item = item)


# User Signup
@app.route('/signup', methods = ['POST', 'GET'])
def signupRestaurant():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        cpassword = request.form['cpassword']

        nan_empty = authenticate.nempty(username = user_name,
            password = password,
            cpassword = cpassword)

        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return render_template('signup.html',
                username = user_name,
                nan_username = nan_empty['err_username'],
                nan_password = nan_empty['err_password'],
                nan_cpassword = nan_empty['err_cpassword'])

        is_valid = authenticate.valid(username = user_name,
            password = password)

        if is_valid is True:
            if password == cpassword:
                hashbrown = authenticate.make_pw_hash(user_name, password)
                user = User(name  = user_name,
                    salt = hashbrown.split('|')[1],
                    hashedpw = hashbrown.split('|')[0])
                session.add(user)
                session.commit()
                user_id = session.query(User.id).order_by(desc(User.dt_added)).limit(1).all()

                login_session['userid'] = user_id
                flash("User created successfully! Welcome %s!" % user_name)

                return redirect(url_for('itemList'))
            else:
                flash("The passwords entered do not match. Please re-enter.")
                return render_template('signup.html', username = user_name)
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('signup.html',
                username = user_name,
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


# User Login
@app.route('/login', methods = ['POST', 'GET'])
def loginSite():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']

        nan_empty = authenticate.nempty(username = user_name,
            password = password)

        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return render_template('login.html', nan_message = nan_empty)

        is_valid = authenticate.valid(username = user_name,
            password = password)

        if is_valid is True:
            username = session.query(User).filter_by(name = user_name).all()

            if username:
                for each in username:
                    salt = each.salt
                    hashedpw = authenticate.make_pw_hash(user_name, password, salt).split('|')[0]
                    try:
                        user = session.query(User).filter_by(hashedpw = hashedpw).one()
                        if user:
                           break
                    except NoResultFound:
                        user = None

                if not user:
                    flash("The entered password was incorrect. Please try again.")
                    return render_template('login.html', username = user_name)
            else:
                flash("User does not exist. Please check your username.")
                return render_template('login.html', username = user_name)

            login_session['userid'] = user.id
            flash("Welcome %s!" % user_name)
            return redirect(url_for('itemList'))
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('login.html',
                username = user_name,
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


# Logs out from the site
@app.route('/logout', methods = ['GET'])
def logoutSite():
    if 'userid' in login_session:
        user_id = escape(login_session.get('userid'))
        username = session.query(User.name).filter_by(id = int(user_id)).one()

        login_session.pop('userid', None)
        flash("Goodbye %s!" % username)

    return redirect(url_for('itemList'))


# Adds a new menu item to a restaurant
@app.route('/catalog/item/add',
    methods = ['POST', 'GET'])
def newItem():
    if request.method == 'GET':
        return render_template('newitem.html')

    if request.method == 'POST':
        if 'userid'  not in login_session:
            flash("Please log in first to add an item.")
            return redirect(url_for('loginSite'))

        if len(request.form['name']) == 0:
            flash("The name of the item is mandatory!")
            return render_template('newitem.html',
                name = request.form['name'],
                price = request.form['price'],
                category = request.form['category'],
                description = request.form['description'])

        user_id = escape(login_session.get('userid'))
        user = session.query(User).filter_by(id = int(user_id)).one()

        new_item = CatalogItem(name = request.form['name'],
            price  = request.form['price'],
            category  = request.form['category'],
            description = request.form['description'],
            user = user)
        session.add(new_item)
        session.commit()

        item = session.query(CatalogItem).order_by(desc(CatalogItem.dt_added)).limit(1).one()
        flash("New item added!")

        return redirect(url_for('viewCatalogItem',
            category = item.category,
            item_id = item.id))


# Edits a single menu item of a restaurant
@app.route('/catalog/item/<int:item_id>/edit',
    methods = ['POST', 'GET'])
def editItem(item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if not item:
        flash("Invalid item. Please check that you have selected a valid item.")
        return redirect(url_for('viewCatalogItem', item_id = item_id))

    if request.method == 'GET':
        return render_template('edititem.html', item = item)

    if request.method == 'POST':
        if 'userid'  not in login_session:
            flash("Please log in first to edit the item.")
            return redirect(url_for('loginSite'))

        user_id = escape(login_session['userid'])

        if user_id == item.user_id:        
            item.name = request.form['name']
            item.price = request.form['price']
            item.category = request.form['category']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            flash("Item saved successfully!")
        else:
            flash("You are not authorized to delete this item!")
            return redirect(url_for('viewCatalogItem',
                category = item.category,
                item_id = item.id))            

        return redirect(url_for('viewCatalogItem', category = item.category, item_id = item.id))


# Deletes a menu item
@app.route('/catalog/item/<int:item_id>/delete',
    methods = ['POST', 'GET'])
def deleteItem(item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if not item:
        flash("Invalid item. Please check that you have selected a valid item.")
        return redirect(url_for('viewCatalogItem', item_id = item_id))

    if request.method == 'GET':
        return render_template('deleteitem.html', item = item)

    if request.method == 'POST':
        if 'userid'  not in login_session:
            flash("Please log in first to delete the item.")
            return redirect(url_for('loginSite'))

        user_id = escape(login_session['userid'])

        if user_id == item.user_id:
            session.delete(item)
            session.commit()
            flash("Item deleted!")
        else:
            flash("You are not authorized to delete this item!")
            return redirect(url_for('viewCatalogItem',
                category = item.category,
                item_id = item.id))

        return redirect(url_for('itemList'))


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
