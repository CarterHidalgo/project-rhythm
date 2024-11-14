# Name: helper.py
# Author: Carter Hidalgo
#
# Purpose: functions for printing colored text

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def blue(text):
    return f"\033[94m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def purple(text):
    return f"\033[95m{text}\033[0m"

def cyan(text):
    return f"\033[96m{text}\033[0m"

def pink(text):
    return f"\033[38;5;200m{text}\033[0m"

def grey(text):
    return f"\033[90m{text}\033[0m"

def orange(text):
    return f"\033[38;5;214m{text}\033[0m"

def light_green(text):
    return f"\033[92m{text}\033[0m"

