import argparse
import os
import socket
import threading

def handle_client(client_socket, directory):
    request = client_socket.recv(1024)
    request_lines = request.decode('utf-8').split('\r\n')
    _, path, _ = request_lines[0].split(' ')
    print(f'Received request for path: {path}')
    if path == '/':
        response = 'HTTP/1.1 200 OK\r\n\r\n'
    elif path.startswith('/files/'):
        if directory is None:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
        else:
            filename = path.split('/')[-1]
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n'
                response = bytes(response_headers, 'utf-8') + file_content
            else:
                response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    elif path.startswith('/echo/'):
        response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'
        response = response_headers + path[6:]
    else:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    client_socket.send(bytes(response, 'utf-8') if isinstance(response, str) else response)
    client_socket.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory')
    args = parser.parse_args()

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, args.directory))
        client_thread.start()

if __name__ == "__main__":
    main()