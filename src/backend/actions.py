# Name: table.py
# Author: Carter Hidalgo
#
# Purpose: link tasks to scara action methods

from backend.scara import Scara
from colors.colors import pink

class Actions:
    def __init__(self):
        self.scara = Scara()

        self.lookup = {
            "height" : self.height,
            "move": self.move,
            "grab": self.grab,
            "release": self.release,
            "reset": self.reset,
        }

        # rough estimations (eyeball)
        # ~14 in radius or 355.6 mm radius

        self.grid = {}
        self.square_zero = (-111.1, 339.7)
        self.grid_gap = 31.75 #abs(self.square_zero[0] * 2) / 7
        self.grid_start = (self.square_zero[0] - (2 * self.grid_gap), self.square_zero[1])

        for x in range(12):
            for y in range(8):
                index = x * 8 + y
                self.grid[index] = (self.grid_start[0] + x * self.grid_gap, self.grid_start[1] - y * self.grid_gap)

    def _print(text):
        print(f"[{pink('scara')}]: {text}")

    def _mm_to_in(self, mm):
        inches = mm / 25.4
        return round(inches, 1)

    def calibrate(self):
        self.scara.calibrate()

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
        
        self.scara.move(self.grid[args[0]][0], self.grid[args[0]][1], True, False)

    def grab(self, args):
        Actions._print("grabs")
        self.scara.grab()

    def release(self, args):
        Actions._print("releases")
        self.scara.release()

    def reset(self, args):
        Actions._print("moves to high height")
        Actions._print("moves to start")
        Actions._print("releases")

    def test_full(self):
        for tup in self.grid:
            self.scara.move(tup[0], tup[1], True)

    def test_small(self, start, end):
        end += 1 # I want a closed range [start, end] not [start, end)
        for x in range(start+16, end+16):
            self.scara.move(self.grid[x+16][0], self.grid[x+16][1], True, False)

    def test_index(self):
        while True:
            index = int(input("Enter square index: "))
            self.scara.move(self.grid[index+16][0], self.grid[index+16][1], True, True)

    def output_grid(self):
        for index in range(96):
            print(f"{index-16}: ({self._mm_to_in(self.grid[index][0])}, {self._mm_to_in(self.grid[index][1])}")
        print(f"grid_size: {self.grid_gap}")

    def do(self, cmd, *args):
        self.lookup[cmd](args)