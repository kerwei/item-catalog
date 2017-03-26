from flask import Blueprint, render_template, abort, jsonify, url_for, redirect, flash, request
from flask import session as login_session
from flask.ext.seasurf import SeaSurf
from jinja2 import TemplateNotFound

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User

authenticate_page = Blueprint('authenticate_page', __name__,
                        template_folder='templates')


# User Signup
@authenticate_page.route('/signup', methods = ['POST', 'GET'])
def signupSite():
    if request.method == 'GET':
        if 'userid' in login_session:
            flash("You are already logged in!")
            return redirect(url_for('public_page.itemList'))

        return render_template('signup.html')

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        cpassword = request.form['cpassword']

        nan_empty = helpers.nempty(username = user_name,
            password = password,
            cpassword = cpassword)

        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return render_template('signup.html',
                username = user_name,
                nan_username = nan_empty['err_username'],
                nan_password = nan_empty['err_password'],
                nan_cpassword = nan_empty['err_cpassword'])

        is_valid = helpers.valid(username = user_name,
            password = password)

        if is_valid is True:
            if password == cpassword:
                hashbrown = helpers.make_pw_hash(user_name, password)
                user = User(name  = user_name,
                    salt = hashbrown.split('|')[1],
                    hashedpw = hashbrown.split('|')[0])
                session.add(user)
                session.commit()
                new_user = dbfunctions.getDescending(User, User.dt_added, 1)

                login_session['userid'] = new_user.id
                flash("User created successfully! Welcome %s!" % user_name)

                return redirect(url_for('public_page.itemList'))
            else:
                flash("The passwords entered do not match. Please re-enter.")
                return render_template('signup.html', username = user_name)
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('signup.html',
                username = user_name,
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


# Logs out from the site
@authenticate_page.route('/logout', methods = ['GET'])
def logoutSite():
    if 'userid' in login_session:
        # user_id = escape(login_session.get('userid'))
        user_id = login_session['userid']
        username = session.query(User.name).filter_by(id = int(user_id)).one()

        login_session.clear()
        # for key in login_session:
        #     login_session.pop(key, None)

        flash("Goodbye %s!" % username)

    return redirect(url_for('public_page.itemList'))