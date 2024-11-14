# Name: table.py
# Author: Carter Hidalgo
#
# Purpose: link tasks to scara action methods

from backend.scara import Scara

class Actions:
    lookup = {
        "height" : Scara.height,
        "move": Scara.move,
        "grab": Scara.grab,
        "release": Scara.release,
        "reset": Scara.reset,
    }

    def do(cmd, *args):
        Actions.lookup[cmd](args)