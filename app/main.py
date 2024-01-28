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
    elif path.startswith('/echo/'):
        response_body = path[6:]
        response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n'
        response = response_headers + response_body
    elif path == '/user-agent':
        user_agent = next((line.split(': ')[1] for line in request_lines[1:] if line.lower().startswith('user-agent')), None)
        if user_agent:
            response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n'
            response = response_headers + user_agent
        else:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
    elif path.startswith('/files/'):
        filename = os.path.join(directory, path[7:])
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                response_body = file.read()
            response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(response_body)}\r\n\r\n'
            response = response_headers.encode('utf-8') + response_body
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    client_socket.send(bytes(response, 'utf-8'))
    client_socket.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default=os.getcwd())
    args = parser.parse_args()

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, args.directory))
        client_thread.start()

if __name__ == "__main__":
    main()