# Name: client.py
# Author: Carter Hidalgo
#
# Purpose: listen for udp ip broadcase and establish tcp connection with raspberry pi

import socket, pickle, time, re
from colors.colors import orange, pink

class Client:
    UDP_PORT = 54321
    TCP_PORT = 12345
    DATA = None
    CONNECTED = False
    RUNNING = True
    WAITING = False

    def _is_valid_addr(addr):
        ip_port_pattern = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)$"
        match = re.match(ip_port_pattern, addr)
        if(not match):
            return False
        
        ip = match.group(1)
        port = match.group(2)

        octets = ip.split(".")
        if(len(octets) != 4 or not all(0 <= int(octet) <= 255 for octet in octets if octet.isdigit())):
            return False

        if(not port.isdigit() or not (1024 <= int(port) <= 65535)):
            return False

        return True

    def _send_and_wait(conn, data):
        try:
            serialized_data = pickle.dumps(list(data.queue))
            conn.sendall(len(serialized_data).to_bytes(4, byteorder="big"))
            conn.sendall(serialized_data)
            Client.DATA = None

            response = ""

            while (not response == "readyok") and Client.RUNNING:
                response = conn.recv(1024).decode()
                if response:
                    print(f"[{pink('scara')}]: {response}")
            
            Client.WAITING = False

        except Exception as e:
            print(f"Error sending tasks: {e}")

    def _listen_to_broadcast():
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.settimeout(5)
        udp_socket.bind(('', Client.UDP_PORT))

        print(f"[{orange('client')}]: listening for UDP broadasts on port {Client.UDP_PORT}...")

        try:
            message, address = udp_socket.recvfrom(1024)
            addr = message.decode().strip()

            if(Client._is_valid_addr(addr)):
                print(f"[{orange('client')}]: received broadast from {addr}")

                return addr
        except Exception:
            print(f"[{orange('client')}]: timeout while trying to connect to server")
            return None
        
    def _connect_to_server(addr):
        if not addr:
            print(f"[{orange('client')}]: closed")
            Client.RUNNING = False
            return

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            ip, port = addr.split(":")
            tcp_socket.connect((ip, int(port)))
            Client.CONNECTED = True
            print(f"[{orange('client')}]: connected")

            while Client.RUNNING:
                if Client.DATA:
                    Client._send_and_wait(tcp_socket, Client.DATA)

                time.sleep(1)
        except Exception as e:
            print(f"[{orange('client')}]: error connecting to server: {e}")
            return
        finally:
            tcp_socket.close()
            print(f"[{orange('client')}]: closed")

    def send_data(data):
        Client.WAITING = True
        Client.DATA = data

    def is_empty():
        return False if Client.DATA else True
    
    def is_connected():
        return Client.CONNECTED 
    
    def is_waiting():
        return Client.WAITING
    
    def is_running():
        return Client.RUNNING
    
    def close():
        Client.RUNNING = False

    def setup():
        print(f"[{orange('client')}]: loaded")
        Client._connect_to_server(Client._listen_to_broadcast())