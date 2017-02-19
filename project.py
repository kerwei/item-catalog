# Standard Library
import pdb

# Third party modules
from flask import Flask
from flask import request, render_template, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local custom modules
import authenticate
from database_setup import Base, Restaurant, MenuItem, User


app = Flask(__name__)

# Starts the database
engine = create_engine('sqlite:///restaurantmenu.db')
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
@app.route('/')
@app.route('/restaurant')
def restaurantList():
    restaurant = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurant = restaurant)


# User Signup
@app.route('/restaurant/signup', methods = ['POST', 'GET'])
def signupRestaurant(username = None, err_username = None, err_password = None):
    if request.method == 'GET':
        return render_template('signup.html', 
            username = username, 
            err_username = err_username, 
            err_password = err_password)

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        cpassword = request.form['cpassword']

        nan_empty = authenticate.nempty(username = user_name, 
            password = password, 
            cpassword = cpassword)
        print nan_empty
        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return render_template('signup.html',
                username = user_name, 
                nan_username = nan_empty['err_username'],
                nan_password = nan_empty['err_password'])

        is_valid = authenticate.valid(username = user_name, 
            password = password)

        if is_valid is True and password == cpassword:
            hashbrown = authenticate.make_pw_hash(user_name, password)
            user = User(name  = user_name,
                salt = hashbrown.split('|')[-1],
                hashedpw = hashbrown.split('|')[0])
            flash("User created successfully!")

            return redirect(url_for('restaurantList'))
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('signup.html',
                username = user_name, 
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


# User Login
@app.route('/restaurant/login', methods = ['POST', 'GET'])
def loginRestaurant(username = None, err_username = None, err_password = None):
    if request.method == 'GET':
        return render_template('login.html', 
            username = username, 
            err_username = err_username, 
            err_password = err_password)

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        cpassword = request.form['cpassword']

        nan_empty = authenticate.nempty(username = user_name, 
            password = password, 
            cpassword = cpassword)

        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return redirect(url_for('signupRestaurant', nan_message = nan_empty))

        is_valid = authenticate.valid(username = user_name, 
            password = password)

        if is_valid is True and password == cpassword:
            hashbrown = authenticate.make_pw_hash(user_name, password)
            user = User(name  = user_name,
                salt = hashbrown.split('|')[-1],
                hashedpw = hashbrown.split('|')[0])
            flash("User created successfully!")

            return redirect(url_for('restaurantList'))
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('login.html',
                username = user_name, 
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


# Displays the menu items of a single restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
def viewMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_local = session.query(MenuItem).filter_by(
        restaurant_id = restaurant_id).all()

    return render_template('menu.html',
        restaurant = restaurant,
        items=menu_local)


# Adds a new menu item to a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/add',
    methods = ['POST', 'GET'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        return render_template('newmenuitem.html',
            restaurant_id = restaurant_id)

    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(
            id = restaurant_id).one()
        new_menuitem = MenuItem(name = request.form['name'],
            price  = request.form['price'],
            course  = request.form['course'],
            description = request.form['description'],
            restaurant = restaurant)
        session.add(new_menuitem)
        session.commit()
        flash("New menu item created!")

        return redirect(url_for('viewMenuItem', restaurant_id = restaurant_id))


# Edits a single menu item of a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
    methods = ['POST', 'GET'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'GET':
        return render_template('editmenuitem.html',
            restaurant_id = restaurant_id,
            item = item)

    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(
            id = restaurant_id).one()
        item.name = request.form['name']
        item.price = request.form['price']
        item.course = request.form['course']
        item.description = request.form['description']
        item.restaurant = restaurant
        session.add(item)
        session.commit()
        flash("Menu item edited!")

        return redirect(url_for('viewMenuItem', restaurant_id = restaurant_id))


# Deletes a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
    methods = ['POST', 'GET'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'GET':
        return render_template('deletemenuitem.html',
            restaurant_id = restaurant_id,
            item = item)

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu item deleted!")

        return redirect(url_for('viewMenuItem', restaurant_id = restaurant_id))


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
