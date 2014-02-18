import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
import os
import os.path
import sys

# Go to previous dir to simulate being on the host, and have the "scrabble"
# folder on the URL when accessing the server. e.g., instead of
# http://host/cgi-bin/api.cgi, have http://host.com/scrabble/cgi-bin/api.cgi.
os.chdir("..")

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
handler.cgi_directories = ["/scrabble/cgi-bin"]
server_address = ("", 8000)

httpd = server(server_address, handler)
httpd.serve_forever()

