import socket
import threading

# Server config
HOST = '127.0.0.1'
PORT = 5000

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # Handle broken clients (optional)
            pass

# Handle incoming messages from a client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat.".encode())
            nicknames.remove(nickname)
            break

# Accept new connections
def receive():
    print(f"Server running on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Receive nickname immediately (no "NICKNAME" prompt)
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        
        broadcast(f"Joined the chat!".encode())
        client.send("Connected to the server!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
