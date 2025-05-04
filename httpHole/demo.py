from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Configure logging
logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def handle_request(request, client_address):
    """
    Handles incoming HTTP requests and logs them.
    """
    # Log the request details
    logging.info(f"Request from {client_address[0]}:{client_address[1]}")
    logging.info(f"Path: {request.path}")
    logging.info(f"Headers:\n{request.headers}")

    # If there's a body (e.g., in POST requests), log it
    content_length = request.headers.get('Content-Length')
    if content_length:
        body = request.rfile.read(int(content_length)).decode('utf-8')
        logging.info(f"Body:\n{body}")

    # Respond based on the path
    if request.path == "/admin":
        response = b"Admin Page"
        content_type = "text/html"
    elif request.path == "/robots.txt":
        response = b"User-agent: *\nDisallow: /private \nAllow: /\n\nSitemap: http://contoso.net/sitemap.xml"
        content_type = "text/plain"
    else:
        response = b"Server UP"
        content_type = "text/html"

    # Send the response
    request.send_response(200)
    request.send_header("Content-type", content_type)
    request.end_headers()
    request.wfile.write(response)

def run_server(host="0.0.0.0", port=80):
    """
    Starts the HTTP server and handles requests.
    """
    def handler(*args):
        # Wrap the handler function to pass the request and client address
        handle_request(*args)

    # Create and start the HTTP server
    server = HTTPServer((host, port), BaseHTTPRequestHandler)
    print(f"Starting HTTP server on {host}:{port}...")
    logging.info(f"HTTP server started on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        logging.info("Server shut down.")
    finally:
        server.server_close()

if __name__ == "__main__":
    run_server()