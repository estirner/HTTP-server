import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        request = client_socket.recv(1024)
        print('Received request:')
        print(request.decode('utf-8'))
        response = 'HTTP/1.1 200 OK\r\n\r\n'
        client_socket.send(bytes(response, 'utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()