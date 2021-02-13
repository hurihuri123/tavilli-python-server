from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebServerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        route = self.path
        body = self.parseJsonBody()
        if route == "/newRequest":
            print(body)
            pass
        elif route == "/newSupplierProduct":
            pass
        else:
            print("Receive new POST with unknown route")


# Helpers ---------------------

    def parseJsonBody(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        return json.loads(body) if body else None


class HttpServer(object):
    def __init__(self, web_server_handler):
        super().__init__()
        self.web_server_handler = web_server_handler

    def listen(self, port):
        try:
            server = HTTPServer(('', port), self.web_server_handler)
            print("Web server running on port %s" % port)
            server.serve_forever()
        except KeyboardInterrupt:
            print(" ^C entered stopping web server...")
            server.socket.close()
