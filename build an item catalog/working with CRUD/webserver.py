
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
##########################################   Objective 1 -- List out all restaurants   ##########################################
                    output += "<h2>"
                    output += restaurant.name
                    output += "</h2>"
##########################################   Objective 2 -- Add Edit and Delete links   #########################################
                    output += "<a href='#'>Edit</a>"
                    output += "</br>"
                    output += "<a href='#'>Delete</a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
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


##########################################   OLD CODE   ##########################################

# class WebServerHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         try:
#             if self.path.endswith("/hello"):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 output = ""
#                 output += "<html><body>"
#                 output += "<h1>Hello!</h1>"
#                 output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
#                 output += "</body></html>"
#                 self.wfile.write(output)
#                 print output
#                 return

#             if self.path.endswith("/hola"):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 output = ""
#                 output += "<html><body>"
#                 output += "<h1>&#161 Hola !</h1>"
#                 output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
#                 output += "</body></html>"
#                 self.wfile.write(output)
#                 print output
#                 return

#             if self.path.endswith("/restaurants"):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 output = ""
#                 output += "<html><body>"
#                 output += "<h2>Urban Burger</h2>"
#                 output += "<h2>Panda Garden</h2>"
#                 output += "<h2>Thyme for That Vegetarian Cuisine</h2>"
#                 output += "<h2>Tony's Bistro</h2>"
#                 output += "<h2>Andala's</h2>"
#                 output += "<h2>Auntie Ann's Dinner</h2>"
#                 output += "<h2>Cocina Y Love</h2>"
#                 output += "</body></html>"
#                 self.wfile.write(output)
#                 print output
#                 return

#         except IOError:
#             self.send_error(404, 'File Not Found: %s' % self.path)

#     def do_POST(self):
#         try:
#             self.send_response(301)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             ctype, pdict = cgi.parse_header(
#                 self.headers.getheader('content-type'))
#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 messagecontent = fields.get('message')
#             output = ""
#             output += "<html><body>"
#             output += " <h2> Okay, how about this: </h2>"
#             output += "<h1> %s </h1>" % messagecontent[0]
#             output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
#             output += "</body></html>"
#             self.wfile.write(output)
#             print output
#         except:
#             pass

# def main():
#     try:
#         port = 8080
#         server = HTTPServer(('', port), WebServerHandler)
#         print "Web Server running on port %s" % port
#         server.serve_forever()
#     except KeyboardInterrupt:
#         print " ^C entered, stopping web server...."
#         server.socket.close()

# if __name__ == '__main__':
#     main()