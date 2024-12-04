# Name: main_display.py
# Author: Carter Hidalgo
#
# Purpose: handle display frontend, user input, and CPUs

import threading, time
from frontend.client import Client
from frontend.controller import Controller

def main():
    network_thread = threading.Thread(target=Client.setup)
    network_thread.start()
    
    while Client.is_running() and not Client.is_connected():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            pass

    if Client.is_connected():
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