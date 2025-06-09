import socket
import threading
import sys

def recv_msg(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\033[92m{msg}\033[0m")  # green text for messages
        except:
            break

def client(server_ip, port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))

    threading.Thread(target=recv_msg, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "/exit":
            sock.send(msg.encode())
            break
        sock.send(msg.encode())

    sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)
    client(sys.argv[1])
