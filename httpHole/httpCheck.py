import http.client
import ssl, sys

def check_server(host, port):
    try:
        if port == 443:
            context = ssl.create_default_context()
            conn = http.client.HTTPSConnection(host, port, context=context, timeout=5)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=5)

        conn.request("GET", "/")
        response = conn.getresponse()
        server_banner = response.getheader("Server")

        print(f"[+] {host}:{port} - Server: {server_banner if server_banner else 'Header not found'}")
        conn.close()
    except Exception as e:
        print(f"[-] {host}:{port} - No response ({e})")

if __name__ == "__main__":
    # check if the script is run with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python httpCheck.py <target_host>")
        sys.exit(1)
    # define the target host and ports to check
    target_host =  sys.argv[1]
    ports = [80, 443, 8080]

    for port in ports:
        check_server(target_host, port)
