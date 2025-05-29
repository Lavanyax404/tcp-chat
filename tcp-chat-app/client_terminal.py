import socket
import threading

# Client config
HOST = '127.0.0.1'
PORT = 5000

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICKNAME':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("An error occurred. Disconnecting...")
            client.close()
            break

# Send messages
def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode())

# Start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
