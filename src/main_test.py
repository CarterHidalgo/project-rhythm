# Name: main_test.py
# Author: Carter Hidalgo
#
# Purpose: provide quick test access to project without full network connection
# Command: source ~/.env/bin/activate

from backend.actions import Actions
from backend.scara import Scara
from time import sleep

actions = Actions()
actions.grab(None)
sleep(1)
actions.release(None)