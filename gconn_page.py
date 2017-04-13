import httplib2
import json
import pdb
import requests

from flask import Blueprint, render_template, url_for, redirect, request
from flask import abort, jsonify, flash, make_response
from flask import session as login_session
# from jinja2 import TemplateNotFound
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import dbfunctions
from dbfunctions import session
from database_setup import Base, User


gconn_page = Blueprint('gconn_page', __name__,
                        template_folder='templates')


# Load API endpoints for Google Plus
gplus_ref = json.loads(open('app_links.json', 'r').read())['web']['gplus']
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connects to Google Plus via OAuth2
@gconn_page.route('/gconnect', methods=['POST'])
def gconnect():
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = gplus_ref['atoken'] % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Checks if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('\
            Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = gplus_ref['userinfo']
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    # Set login session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists. If not, add the user to the database.
    user_gp = dbfunctions.getUserByEmail(login_session['email'])
    if not user_gp:
        user_id = dbfunctions.createUser(login_session)
        login_session['user_id'] = user_id
    else:
        login_session['user_id'] = user_gp.id

    welcome = open('templates/oauth_welcome.html').read()
    welcome = welcome % (login_session['username'], login_session['picture'])
    flash("you are now logged in as %s" % login_session['username'])

    return welcome


# Disconnects from Google Plus
@gconn_page.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    # If user is not connected
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Invokes the logout API end point
    url = gplus_ref['revoke'] % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Clears the login session
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        flash("Successfully disconnected!")
        return redirect(url_for('public_page.itemList'))

    else:
        response = make_response(json.dumps('\
            Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'

    return response
