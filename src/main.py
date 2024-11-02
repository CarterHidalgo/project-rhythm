# Name: main.py
# Author: Carter Hidalgo
#
# Purpose: main method for the program

from controller import Controller

def main():
    try:
        controller = Controller()

        while controller.is_running():
            controller.run()
        else:
            controller.close()
    except KeyboardInterrupt:
        controller.close()

if __name__ == "__main__":
    main()