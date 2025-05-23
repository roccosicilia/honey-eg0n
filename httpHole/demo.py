from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class RequestLoggerHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        # Log the request to a file
        self.log_request_to_file()

        # Respond with a blank page
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Are you a bot?")
    
    def do_GET(self):
        # Log the request to a file
        self.log_request_to_file()

        if self.path == "/admin": # Respond with Admin Page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Admin Page")
            return
        elif self.path == "/robots.txt": # Respond with robots.txt
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"User-agent: *\nDisallow: /private \nAllow: /\n\nSitemap: http://contoso.net/sitemap.xml")
            return
        else: # Respond with a blank page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Server UP")

    def do_POST(self):
        # Log the request to a file
        self.log_request_to_file()

        # Respond with a blank page
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Server UP")  # Blank response

    def log_request_to_file(self):
        # Log the request details
        logging.info(f"{self.command} Request from {self.client_address[0]}:{self.client_address[1]}")
        logging.info(f"Path: {self.path}")
        logging.info(f"Headers:\n{self.headers}")

        # If there's a body (e.g., in POST requests), log it
        content_length = self.headers.get('Content-Length')
        if content_length:
            body = self.rfile.read(int(content_length)).decode('utf-8')
            logging.info(f"Body:\n{body}")

def run(server_class=HTTPServer, handler_class=RequestLoggerHandler, port=80):
    logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()