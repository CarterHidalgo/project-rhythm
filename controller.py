# Name: controller.py
# Author: Carter Hidalgo
#
# Purpose: Run the SCARA robot by listening for UCI commands, creating tasks from them, and calling the appropriate robot commands

"""
start server thread

while True:
    String cmd = server.nextCommand()
    String move = getMove(cmd)

    if(move is uci bestmove):
        Stack tasks = getTasks(move)
        for task in tasks:
            do task

    
    server.sendUCIResponse()
"""
from table import do

