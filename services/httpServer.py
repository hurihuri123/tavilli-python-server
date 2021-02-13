from http.server import HTTPServer


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
