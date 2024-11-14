# Name: robot.py
# Author: Carter Hidalgo
#
# Purpose: Provide methods for controlling the scara

from colors.colors import pink

class Scara:
    def _print(text):
        print(f"[{pink('scara')}]: {text}")

    def height(args):
        if(len(args) != 1):
            print(f"Expected 1 argument in setHeight but found {len(args)}")
            return
        
        if(args[0] == 'p'):
            Scara._print("moves to pawn height")
        elif(args[0] == 'n'):
            Scara._print("moves to knight height")
        elif(args[0] == 'b'):
            Scara._print("moves to bishop height")
        elif(args[0] == "r"):
            Scara._print("moves to rook height")
        elif(args[0] == "q"):
            Scara._print("moves to queen height")
        elif(args[0] == "k"):
            Scara._print("moves to king height")
        elif(args[0] == "h"):
            Scara._print("moves to high height")
        else:
            Scara._print(f"WARNING: Invalid height param sent {args[0]}")

    def move(args):
        if(len(args) != 1):
            Scara._print(f"WARNING: Expected 1 argument in move but found {len(args)}")
            return

        if(args[0] < -16):
            Scara._print(f"WARNING: Index {args[0]} out of range")
        elif(args[0] < 0):
            Scara._print(f"moves to white sideline {args[0]}")
        elif(args[0] < 64):
            Scara._print(f"moves to square {args[0]}")
        elif(args[0] < 81):
            Scara._print(f"moves to black sideline {args[0]}")
        else:
            Scara._print(f"WARNING: Index {args[0]} out of range")

    def grab(args):
        Scara._print("grabs")

    def release(args):
        Scara._print("releases")

    def reset(args):
        Scara._print("moves to high height")
        Scara._print("moves to start")
        Scara._print("releases")
