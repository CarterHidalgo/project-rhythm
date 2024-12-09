# Name: main_test.py
# Author: Carter Hidalgo
#
# Purpose: provide quick test access to project without full network connection
# Command: source ~/.env/bin/activate

from backend.scara import Scara
from time import sleep

scara = Scara()

scara.test()
