# Name: main_rpi.py
# Author: Carter Hidalgo
#
# Purpose: handle rpi backend network connection and scara movement
# VM Command: source ~/.env/bin/activate

import socket, threading, pickle, time
from backend.actions import Actions
from colors.colors import light_green

stop_broadcasting = threading.Event()

def _get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"

    return ip

def broadcast_ip():
    ip = _get_ip()
    port = 12345
    broadcast_port = 54321

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = f"{ip}:{port}"
    print(f"[{light_green('rpi')}]: broadcasting IP message: {message}")
    while not stop_broadcasting.is_set():
        sock.sendto(message.encode(), ('<broadcast>', broadcast_port))
        time.sleep(2)

def start_server():
    host = '0.0.0.0'
    port = 12345
    action = Actions()
    running = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((host, port))
        tcp_socket.listen(1)

        print(f"[{light_green('rpi')}]: listening on {host}:{port}")

        conn, addr = tcp_socket.accept()
        stop_broadcasting.set()
        print(f"[{light_green('rpi')}]: connected by {addr}. stopping broadcasting")

        while running:
            try:
                data_len = int.from_bytes(conn.recv(4), byteorder="big")
                serialized_data = conn.recv(data_len)
                tasks = pickle.loads(serialized_data)

                while tasks:
                    print(tasks)
                    cmd, args = tasks.pop(0)
                    action.do(str(cmd), str(args))
                
                conn.send("readyok".encode())
            
            except Exception as e:
                print(f"[{light_green('rpi')}]: Error receiving tasks: {e}")
                running = False

def main():
    broadcast_thread = threading.Thread(target=broadcast_ip)
    broadcast_thread.start()

    start_server()

if __name__ == "__main__":
    main()