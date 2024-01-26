import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
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
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        client_socket.send(bytes(response, 'utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()