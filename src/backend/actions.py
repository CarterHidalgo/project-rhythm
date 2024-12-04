# Name: table.py
# Author: Carter Hidalgo
#
# Purpose: link tasks to scara action methods

from backend.scara import Scara
from colors.colors import pink

class Actions:
    def __init__(self):
        self.lookup = {
            "height" : self.height,
            "move": self.move,
            "grab": self.grab,
            "release": self.release,
            "reset": self.reset,
        }
        self.grid = {}
        self.grid_start = (-300, 400) # (x, y) pos of leftmost, lowest grid in mm
        self.grid_gap = abs(self.grid_start[0] * 2) / 11 # size of grid "square" in mm

        for x in range(12):
            for y in range(8):
                index = x * 8 + y - 16
                self.grid[index] = (self.grid_start[0] + x * self.grid_gap, self.grid_start[1] - y * self.grid_gap)
        
        for i in range(96):
            print(str(i-16) + ": " + str(self.grid[i-16]))

    def _print(text):
        print(f"[{pink('scara')}]: {text}")

    def height(self, args):
        if(len(args) != 1):
            print(f"Expected 1 argument in setHeight but found {len(args)}")
            return
        
        if(args[0] == 'p'):
            Actions._print("moves to pawn height")
        elif(args[0] == 'n'):
            Actions._print("moves to knight height")
        elif(args[0] == 'b'):
            Actions._print("moves to bishop height")
        elif(args[0] == "r"):
            Actions._print("moves to rook height")
        elif(args[0] == "q"):
            Actions._print("moves to queen height")
        elif(args[0] == "k"):
            Actions._print("moves to king height")
        elif(args[0] == "h"):
            Actions._print("moves to high height")
        else:
            Actions._print(f"WARNING: Invalid height param sent {args[0]}")

    def move(self, args):
        if(len(args) != 1):
            Actions._print(f"WARNING: Expected 1 argument in move but found {len(args)}")
            return

        if(args[0] < -16):
            Actions._print(f"WARNING: Index {args[0]} out of range")
            return
        elif(args[0] < 0):
            Actions._print(f"moves to white sideline {args[0]}")
        elif(args[0] < 64):
            Actions._print(f"moves to square {args[0]}")
        elif(args[0] < 80):
            Actions._print(f"moves to black sideline {args[0]}")
        else:
            Actions._print(f"WARNING: Index {args[0]} out of range")
            return
        
        Scara.move(Scara.grid[args[0]])

    def grab(self, args):
        Actions._print("grabs")

    def release(self, args):
        Actions._print("releases")

    def reset(self, args):
        Actions._print("moves to high height")
        Actions._print("moves to start")
        Actions._print("releases")

    def do(self, cmd, *args):
        Actions.lookup[cmd](args)