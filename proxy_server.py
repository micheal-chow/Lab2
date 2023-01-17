import socket

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# proxy client makes request to proxy server
# ps accepts request and sends request to google on behalf of pc
# google will respond to ps
# ps will relay googles information back to pc

# ps will be a program that has both server and client sockets
# client for google, server for pc

def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR)

        data = client_socket.recv(BYTES_TO_READ)
        result = b''+data

        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''

        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data

        response = send_request("www.google.com", 80, request)

        conn.sendall(response)    

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
        # this '2' parameter specifies how much of a queue to allow
        # if conn is being created to server and someone tries to make another at same time,
        # we keep second conn in queue then process in order, default one
        # beyond queue gets connection refused error

        conn, addr = server_socket.accept()

        handle_connection(conn, addr)
        
    

start_server()