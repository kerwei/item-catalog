import hashlib
import pdb
import random
import re
import string

import constants


'''Helper functions for the application'''

# Make hash with secret
def roast_chip(chip):
    return '%s|%s' % (chip, hashlib.sha256(chip + constants.SECRET).hexdigest())

# Generate salt
def make_salt():
    return ''.join(random.sample(string.letters,constants.SALT_LENGTH))

# Make password hash
def make_pw_hash(name, pw):
    x = make_salt()
    return "%s|%s" % (hashlib.sha256(name + pw + x).hexdigest(),x)

# Validates the input username
def valid_username(username):
    return username and constants.USER_RE.match(username)

# Validates the input password
def valid_password(password):
    return password and constants.PASS_RE.match(password)

# Validates the input email
def valid_email(email):
    return not email or constants.EMAIL_RE.match(email)

# Validates the integrity of cookies
def valid_cookie(cookie):
    if cookie:
        dough = cookie.split('|')[0]
        return roast_chip(dough) == cookie

# Checks the validity of all input fields
def valid(**kwargs):
    err_username = None
    err_password = None
    err_email = None

    if kwargs['username']:
        if valid_username(kwargs['username']) is None:
            err_username = "Please enter a valid username."

    if kwargs['password']:
        if valid_password(kwargs['password']) is None:
            err_password = "Please enter a valid password."

    if (err_username is not None) | (err_password is not None):
        return {'err_username': err_username, 'err_password': err_password,}
    else:
        return True


# Checks that the inputs are not empty
def nempty(**kwargs):
    err_username = None
    err_password = None
    err_cpassword = None
    
    if len(kwargs['username']) == 0:
        err_username = "Please enter a user name."

    if len(kwargs['password']) == 0:
        err_password = "Please enter a password."

    if len(kwargs['cpassword']) == 0:
        err_cpassword = "Please re-enter your password."

    if len(kwargs['username']) * \
    len(kwargs['password']) * len(kwargs['cpassword']) == 0:
        return {'err_username': err_username, 
        'err_password': err_password,
        'err_cpassword': err_cpassword}
    else:
        return True
