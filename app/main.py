import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        request = client_socket.recv(1024)
        request_lines = request.decode('utf-8').split('\r\n')
        start_line = request_lines[0].split(' ')
        method, path, version = start_line
        print(f'Received request for path: {path}')
        if path == '/':
            response = 'HTTP/1.1 200 OK\r\n\r\n'
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        client_socket.send(bytes(response, 'utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()