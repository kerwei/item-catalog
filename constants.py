import re
from time import gmtime, strftime


# Number of salt characters
SALT_LENGTH = 5
# Username needs to be alphanumeric between 3 and 20 characters
# Includes "-" and "_"
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
# Password needs to be any characters between 3 and 20 characters
PASS_RE = re.compile(r"^.{3,20}$")
# Standard format for email.
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
# Secret for username and password hashing
SECRET = 'TERCES'
# Not used for this project
# Used for the expiration of cookies
EXP_TIME = strftime("%a %d %b %Y %X", gmtime(-1)) + ' GMT'
# Possibly not used
URL_RE = re.compile(r"^https:\/\/[a-z.]*|^http:\/\/localhost:5000")
