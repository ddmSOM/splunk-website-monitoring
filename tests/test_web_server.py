import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import base64
from StringIO import StringIO

class Handler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        username = 'admin'
        password = 'changeme'
        
        encoded_password = base64.b64encode(username + ":" + password)
        
        # Present header reflection page
        if self.path == "/header_reflection":
            self.do_HEAD()
            self.wfile.write('<html><body><div class="user-agent">%s</div></body></html>' % str(self.headers['user-agent']))
            
        # Check the user-agent and return 201 when the user-agent is "USER_AGENT_CHECK"
        if self.path == "/user_agent_check":
            
            if 'user-agent' in self.headers and self.headers['user-agent'] == 'USER_AGENT_CHECK':
                self.send_response(201)
            else:
                print "user-agent was not set to 'USER_AGENT_CHECK'"
            
            self.do_HEAD()
            self.wfile.write('<html><body></body></html>')
            
            
        # Present the HTML page with no authentication
        if self.path == "/test_page":
            self.do_HEAD()
            
            with open( os.path.join("web_files", "test_page.html"), "r") as webfile:
                self.wfile.write(webfile.read())#.replace('\n', '')
        
        # Present the HTML page with optional authentication
        elif self.path == "/optional_auth":
            
            if self.headers.getheader('Authorization') == None:
                self.send_response(202)
                self.wfile.write('not authenticated')
            
            elif self.headers.getheader('Authorization') == ('Basic ' + encoded_password):
                self.send_response(203)
                self.wfile.write('authenticated')
            
            
        # Present frontpage with user authentication.
        elif self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            
        elif self.headers.getheader('Authorization') == ('Basic ' + encoded_password):
            self.do_HEAD()
            #self.wfile.write(self.headers.getheader('Authorization'))
            #self.wfile.write('authenticated!')
            
            with open( os.path.join("web_files", "test_page.html"), "r") as webfile:
                self.wfile.write(webfile.read())#.replace('\n', '')
            
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
     
def get_server(port):
    """
    Call httpd.shutdown() to stop the server
    """
    
    httpd = SocketServer.TCPServer(("", port), Handler)
    return httpd
