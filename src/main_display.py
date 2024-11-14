# Name: main.py
# Author: Carter Hidalgo
#
# Purpose: handle display frontend, user input, and CPUs

import threading, time
from frontend.client import Client
from frontend.controller import Controller

def main():
    network_thread = threading.Thread(target=Client.setup)
    network_thread.start()
    
    while not Client.is_connected():
        time.sleep(1)

    try:
        controller = Controller()

        while controller.is_running():
            controller.run()
        else:
            controller.close()
    except KeyboardInterrupt:
        controller.close()
    finally:
        Client.close()
        network_thread.join()


if __name__ == "__main__":
    main()