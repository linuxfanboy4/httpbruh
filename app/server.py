import os
import socket

def serve_file(file_path, client_socket):
    try:
        with open(file_path, 'rb') as file:
            client_socket.sendall(b"HTTP/1.1 200 OK\r\n")
            content_type = "text/html" if file_path.endswith('.html') else "text/css" if file_path.endswith('.css') else "application/javascript"
            client_socket.sendall(f"Content-Type: {content_type}\r\n\r\n".encode())
            client_socket.sendall(file.read())
    except Exception:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found")

def start_server():
    host = '0.0.0.0'
    port = int(input("Enter the port to start the server on: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        if request:
            requested_file = request.split(' ')[1][1:] or "index.html"
            if requested_file.endswith(".html") or requested_file.endswith(".css") or requested_file.endswith(".js"):
                file_path = os.path.join(os.getcwd(), requested_file)
                if os.path.exists(file_path):
                    serve_file(file_path, client_socket)
                else:
                    client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found")
            else:
                client_socket.sendall(b"HTTP/1.1 415 Unsupported Media Type\r\n\r\nUnsupported File Type")
        client_socket.close()

if __name__ == "__main__":
    start_server()
