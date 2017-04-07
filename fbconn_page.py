import json
import httplib2
import pdb

from flask import Blueprint, render_template, abort, jsonify, url_for, redirect, request
from flask import session as login_session
from jinja2 import TemplateNotFound
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import dbfunctions
from dbfunctions import session
from database_setup import Base, CatalogItem, User

fbconn_page = Blueprint('fbconn_page', __name__,
                        template_folder='templates')


# Load API endpoints for FB Connect
fb_ref = json.loads(open('app_links.json', 'r').read())['web']['fbconn']


@fbconn_page.route('/fbconnect', methods=['POST'])
def fbconnect():
    # if request.args.get('state') != login_session['state']:
    #     response = make_response(json.dumps('Invalid state parameter.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = fb_ref['atoken'] % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = fb_ref['nameid'] % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # pdb.set_trace()
    for k, v in data: print k
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout,
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = fb_ref['picture'] % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_fb = helpers.getUserByEmail(login_session['email'])
    if not user_fb:
        user_id = helpers.createUser(login_session)
    login_session['user_id'] = user_id

    welcome = open('templates/oauth_welcome.html').read()
    welcome = welcome % (login_session['username'], login_session['picture'])
    flash("Now logged in as %s" % login_session['username'])
    return output


@fbconn_page.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = fb_ref['revoke'] % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"