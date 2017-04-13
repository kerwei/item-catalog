from flask import Blueprint, render_template, url_for, redirect, request
from flask import abort, jsonify, flash
from flask import session as login_session
from flask.ext.seasurf import SeaSurf
# from jinja2 import TemplateNotFound

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User


authenticate_page = Blueprint('authenticate_page', __name__,
                        template_folder='templates')


# User Signup
@authenticate_page.route('/signup', methods=['POST', 'GET'])
def signupSite():
    if request.method == 'GET':
        # Cases where users access the signup page via the URL
        # Redirects the users back to the main landing page if they're already
        # logged in.
        if 'userid' in login_session:
            flash("You are already logged in!")
            return redirect(url_for('public_page.itemList'))

        # Displays the signup page, otherwise
        return render_template('signup.html')

    if request.method == 'POST':
        # Gets the form details
        user_name = request.form['name']
        password = request.form['password']
        cpassword = request.form['cpassword']
        # Checks that the required fields are non-empty
        nan_empty = helpers.nempty(username=user_name,
            password=password,
            cpassword=cpassword)

        if nan_empty is not True:
            # Throws error messages if there are empty fields. Retains the
            # user name.
            flash("Please ensure all fields are filled before submitting.")
            return render_template('signup.html',
                username=user_name,
                nan_username=nan_empty['err_username'],
                nan_password=nan_empty['err_password'],
                nan_cpassword=nan_empty['err_cpassword'])

        # Checks that the entered user name and password meet the requirements
        is_valid = helpers.valid(username=user_name,
            password=password)

        # Proceeds if validation is successful
        if is_valid is True:
            # Ensures that the password was indeed entered as intended
            if password == cpassword:
                # Generates the hashed password based on a random salt
                hashbrown = helpers.make_pw_hash(user_name, password)
                # Creates the User and persist it to the database
                user = User(name=user_name,
                    salt=hashbrown.split('|')[1],
                    hashedpw=hashbrown.split('|')[0])
                session.add(user)
                session.commit()
                # Retrieves the entry that was just added to the database.
                # Signs the user in and sets the login session automatically.
                new_user = dbfunctions.getDescending(User, User.dt_added, 1)
                login_session['userid'] = new_user.id
                login_session['username'] = new_user.name
                login_session['auth_type'] = "local"

                flash("User created successfully! Welcome %s!" % user_name)
                return redirect(url_for('public_page.itemList'))
            else:
                # Throws the password-not-matched error
                flash("The passwords entered do not match. Please re-enter.")
                return render_template('signup.html', username=user_name)
        else:
            # Throws the error if the entered username/password do not meet
            # requirements. Retains the username.
            flash("Username/password not valid. Please re-enter.")
            return render_template('signup.html',
                username=user_name,
                err_username=is_valid['err_username'],
                err_password=is_valid['err_password'])


# Logs out from the site
@authenticate_page.route('/logout', methods=['GET'])
def logoutSite():
    # Checks if the user is logged through OAuth2. Redirects to the
    # corresponding functions as necessary.
    if 'auth_type' not in login_session:
        if 'gplus_id' in login_session:
            return redirect(url_for('gconn_page.gdisconnect'))
        else:
            return redirect(url_for('fbconn_page.fbdisconnect'))

    # Clears the login session and redirects back to the main landing page
    if 'username' in login_session:
        username = login_session['username']
        login_session.clear()
        flash("Goodbye %s!" % username)

    return redirect(url_for('public_page.itemList'))
