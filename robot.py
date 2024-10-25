# Name: robot.py
# Author: Carter Hidalgo
#
# Purpose: Provide methods for controlling the scara

def height(args):
    if(len(args) != 1):
        print(f"WARNING: Expected 1 argument in setHeight but found {len(args)}")
        return
    
    if(args[0] == 'pawn'):
        print("robot moves to pawn height")
    elif(args[0] == 'knight'):
        print("robot moves to knight height")
    elif(args[0] == 'bishop'):
        print("robot moves to bishop height")
    elif(args[0] == "rook"):
        print("robot moves to rook height")
    elif(args[0] == "queen"):
        print("robot moves to queen height")
    elif(args[0] == "king"):
        print("robot moves to king height")
    elif(args[0] == "high"):
        print("robot moves to high height")
    else:
        print(f"WARNING: Invalid height sent {args[0]}")

def move(args):
    if(len(args) != 1):
        print(f"WARNING: Expected 1 argument in move but found {len(args)}")
        return

    if(args[0] < -16):
        print(f"WARNING: Index {args[0]} out of range")
    elif(args[0] < 0):
        print(f"robot moves to white sideline {args[0]}")
    elif(args[0] < 64):
        print(f"robot moves to square {args[0]}")
    elif(args[0] < 81):
        print(f"robot moves to black sideline {args[0]}")
    else:
        print(f"WARNING: Index {args[0]} out of range")

def grab(args):
    print("robot grabs")

def release(args):
    print("robot releases")

def reset(args):
    print("robot moves to high height")
    print("robot moves to start")
    print("robot releases")

