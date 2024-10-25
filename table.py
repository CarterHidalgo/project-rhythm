# Name: table.py
# Author: Carter Hidalgo
#
# Purpose: Provide a lookup table for scara actions based on flags from the task stack

from robot import *

_actions = {
    "height" : height,
    "move": move,
    "grab": grab,
    "release": release,
    "reset": reset,
}

def do(command, *args):
    _actions[command](args)
