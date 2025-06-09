import socket
import threading
from datetime import datetime

clients = {}
lock = threading.Lock()

def broadcast(msg, exclude=None):
    with lock:
        for c in clients.values():
            if c != exclude:
                try:
                    c.send(msg.encode())
                except:
                    pass

def handle_client(client_socket, addr):
    try:
        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        with lock:
            clients[username] = client_socket
        broadcast(f"[{timestamp()}] {username} joined the chat.")

        while True:
            msg = client_socket.recv(1024).decode()
            if not msg or msg.lower() == "/exit":
                break
            broadcast(f"[{timestamp()}] {username}: {msg}", exclude=client_socket)

    except:
        pass
    finally:
        with lock:
            if username in clients:
                del clients[username]
        broadcast(f"[{timestamp()}] {username} left the chat.")
        client_socket.close()

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

def server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server running on {host}:{port}")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    server()
