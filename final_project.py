# Standard Library
import pdb

# Third party modules
from flask import Flask
from flask import request, render_template, redirect, url_for, flash, jsonify
from flask import session as login_session
from flask.ext.seasurf import SeaSurf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests

# Local custom modules
import helpers
from helpers import valid_statetoken
from database_setup import Base, CatalogItem, User
import dbfunctions
from dbfunctions import session
from public_page import public_page
from private_page import private_page
from authenticate_page import authenticate_page
from gconn_page import gconn_page
from fbconn_page import fbconn_page


app = Flask(__name__)
app.register_blueprint(public_page)
app.register_blueprint(authenticate_page)
app.register_blueprint(private_page)
app.register_blueprint(gconn_page)
app.register_blueprint(fbconn_page)

csrf = SeaSurf(app)

# Constants
APPLICATION_NAME = "Item Catalog App"


# User Login
@csrf.exempt
@app.route('/login', methods = ['POST', 'GET'])
def loginSite():
    if request.method == 'GET':
        if 'userid' in login_session:
            flash("You are already logged in!")
            return redirect(url_for('public_page.itemList'))

        login_session['state'] = helpers.gen_state()
        return render_template('login.html', STATE = login_session['state'])

    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']

        nan_empty = helpers.nempty(username = user_name,
            password = password)

        if nan_empty is not True:
            flash("Please ensure all fields are filled before submitting.")
            return render_template('login.html', nan_message = nan_empty)

        is_valid = helpers.valid(username = user_name,
            password = password)

        if is_valid is True:
            username = session.query(User).filter_by(name = user_name).all()

            if username:
                for each in username:
                    salt = each.salt
                    hashedpw = helpers.make_pw_hash(user_name,
                        password,
                        salt).split('|')[0]
                    try:
                        user = session.query(User).filter_by(
                            hashedpw = hashedpw).one()
                        if user:
                           break
                    except NoResultFound:
                        user = None

                if not user:
                    flash("The entered password was incorrect. \
                        Please try again.")
                    return render_template('login.html', username = user_name)
            else:
                flash("User does not exist. Please check your username.")
                return render_template('login.html', username = user_name)

            csrf_token = helpers.roast_chip(str(user.id) + user.name)
            login_session['userid'] = user.id
            login_session['username'] = user.name
            login_session['picture'] = user.picture
            login_session['email'] = user.email
            login_session['auth_type'] = "local"
            flash("Welcome %s!" % user_name)
            return redirect(url_for('public_page.itemList'))
        else:
            flash("Username/password not valid. Please re-enter.")
            return render_template('login.html',
                username = user_name,
                err_username = is_valid['err_username'],
                err_password = is_valid['err_password'])


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
