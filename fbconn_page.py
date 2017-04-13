import json
import httplib2
import pdb

from flask import Blueprint, render_template, url_for, redirect
from flask import abort, jsonify, request, flash
from flask import session as login_session
# from jinja2 import TemplateNotFound
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User


fbconn_page = Blueprint('fbconn_page', __name__,
                        template_folder='templates')

# Load the API endpoints for FB Connect
fb_ref = json.loads(open('app_links.json', 'r').read())['web']['fbconn']


# Prepares the URL and requests for the required API data.
# Returns the response data as a JSON object
def getapidata(urlref, *args):
    # Prepares the URL call
    url = urlref % (args)
    # Request for and parses the API data as JSON
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    return json.loads(result)


# Connects to the FBconnect Graph API
@fbconn_page.route('/fbconnect', methods=['POST'])
def fbconnect():
    access_token = request.data
    # Reads the client id and app secret
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    # Gets the access token
    atoken_data = getapidata(fb_ref['atoken'],
        app_id,
        app_secret, access_token)
    token = atoken_data['access_token']

    # Gets the user info
    user_data = getapidata(fb_ref['nameid'], token)
    login_session['provider'] = "facebook"
    login_session['username'] = user_data['name']
    login_session['email'] = user_data['email']
    login_session['facebook_id'] = user_data['id']

    # The token must be stored in the login_session in order to properly logout
    login_session['token'] = token

    # Gets the user profile picture
    pic_data = getapidata(fb_ref['picture'], user_data['id'])
    login_session['picture'] = pic_data["data"]["url"]

    # see if user exists
    user_fb = dbfunctions.getUserByEmail(login_session['email'])
    if not user_fb:
        user_id = dbfunctions.createUser(login_session)
        login_session['user_id'] = user_id
    else:
        login_session['user_id'] = user_fb.id

    welcome = open('templates/oauth_welcome.html').read()
    welcome = welcome % (login_session['username'], login_session['picture'])
    flash("Now logged in as %s" % login_session['username'])
    return welcome


# Revokes the access to the FBconnect Graph API
@fbconn_page.route('/fbdisconnect')
def fbdisconnect():
    fb_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['token']

    # Invokes the logout API call and clears the login session
    logout_data = getapidata(fb_ref['revoke'], fb_id, access_token)
    del login_session['token']
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    flash("Successfully disconnected!")

    return redirect(url_for('public_page.itemList'))
