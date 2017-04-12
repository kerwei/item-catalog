# Project: Item Catalog
This simple Flask application allows registered users to create and maintain a 
personal catalog of items. Catalog items are available for viewing by the public
but only the owner of the items has the authority to edit or delete them. Users
may register themselves directly through the site, or by OAuth2 authentication,
which provides access for Google Plus and Facebook Connect.

Cross Site Reference Forgery (CSRF) attacks are taken into consideration in the
design of this application and is taken care of by the Flask-Seasurf extension.

1. APPLICATION SETUP
Flask (0.10.1)
Flask-SeaSurf (0.2.2)
SQL Alchemy (0.8.4)
OAuth2Client (4.0.0)

2. INSTRUCTIONS
a. The application is pre-loaded with a mock database for demonstration only.
To start from a clean slate, delete 'catalogitem.db' from the root folder and
run the 'database_setup.py' file from your python console. This will create
a new database, ready with empty User and CatalogItem tables.

b. If you deleted the 'catalogitem.db' file by mistake, and wish to start the
application with the pre-loaded mock database, simply run 'lotsofitem.py' from
your python console after you have completed step 2a.

c. Finally, launch the application by running the 'final_project.py' file from
your python console. 