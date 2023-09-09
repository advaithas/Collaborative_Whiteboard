import socket
import threading

# Define host and port
HOST = '127.0.0.1'
PORT = 8000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# List to store all client connections
clients = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "clear":
                for c in clients:
                    c.send(message.encode())
            else:
                for c in clients:
                    if c != client_socket:
                        c.send(message.encode())
        except:
            # Handle errors
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to continuously accept new connections
def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start thread to accept new connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
