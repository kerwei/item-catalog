import datetime
import cgi

import pdb
from sqlalchemy import create_engine
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import sessionmaker
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from database_setup import Base, MenuItem, Restaurant


# Starts the database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurant"):
            # Get all restaurant names
            rstrs = session.query(Restaurant).all()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h3>List of restaurants</h3>"
            message += "<ul>"
            for r in rstrs:
                message += "<li>%s</li>" % (r.name)
                message += "<a href=""/restaurant/%s/edit"">Edit</a>" % (r.id)
                message += "<a href=""/restaurant/%s/delete"">Delete</a>" % (r.id)
            message += "<ul>"
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/restaurant/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h3>Add a restaurant</h3>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Gets the restaurant id from path
            restaurant_id = self.path.split('/')[-2]

            # Queries for the restaurant name by id
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            message = ""
            message += "<html><body>"
            message += "<h3>Rename a restaurant</h3>"
            message += "<h5>Old name:</h5><p>%s</p>" % (restaurant.name)
            message += "<h5>New name:</h5>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>''' % (restaurant_id)
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/delete"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Gets the restaurant id from path
            restaurant_id = self.path.split('/')[-2]

            # Queries for the restaurant name by id
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

            message = ""
            message += "<html><body>"
            message += "<h3>Delete a restaurant</h3>"
            message += "<p>Hit 'Submit' to delete <b>%s</b></p>" % (restaurant.name)
            message += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'><input type="submit" value="Submit"> </form>''' % (restaurant_id)
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    field_input = fields.get('restaurant_name')

                    # Adds the new restaurant to the database
                    new_restaurant = Restaurant(name = field_input[0])
                    session.add(new_restaurant)
                    session.commit()
            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    field_input = fields.get('restaurant_name')

                    # Updates the name of the restaurant
                    # Gets the restaurant id from path
                    restaurant_id = self.path.split('/')[-2]

                    # Queries for the restaurant name by id
                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    restaurant.name = field_input[0]
                    session.add(restaurant)
                    session.commit()
            elif self.path.endswith("/delete"):
                # Deletes the restaurant
                # Gets the restaurant id from path
                restaurant_id = self.path.split('/')[-2]

                # Queries for the restaurant name by id
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                session.delete(restaurant)
                session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurant')
            self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
