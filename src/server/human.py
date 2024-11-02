# Name: human.py
# Author: Carter Hidalgo
#
# Purpose: methods for sending uci commands from humans

import os
from helper.board import Board
from helper.colors import yellow, green, cyan
from helper.paths import stockfish_path
from server.engine import Engine

class Human:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.time = Board.play_time
        self.teacher = Engine(stockfish_path, "stockfish", "grey", True)
        print(f"[{self._text('server', 'yellow')}]: loaded [{self._text(self.name, self.color)}]")

    def _text(self, text, color):
        if color == "yellow":
            return yellow(text)
        elif color == "green":
            return green(text)
        elif color == "cyan":
            return cyan(text)
        else:
            return text 

    def _print_help(self):
        print(f"[{self._text('server', 'yellow')}]:")
        print('\n > Use the keyboard to enter moves in algebraic notation e.g. "e2e4"')
        print(' > Type "moves" to display a list of all legal moves')
        print(' > Type "board" to print the current board state')
        print(' > Type "quit" to quit the program')
        print()

    def get_time(self):
        return int(self.time)
    
    def sub_time(self, time):
        self.time -= time

    def send_and_wait(self, ignore, ignore2):
        perft_list = sorted(self.teacher.get_perft(), key=lambda x: (x[0], int(x[1]), x[2], int(x[3])))

        while True:
            print(f"[{self._text(self.name, self.color)}]: ", end="")
            bestmove = input()
            if bestmove in perft_list:
                return bestmove
            elif bestmove == "help":
                self._print_help()
            elif bestmove == "moves":
                print(f"[{self._text('server','yellow')}]: ")
                for move in perft_list:
                    print(f" > {move}")
                print()
            elif bestmove == "board":
                Board.print()
            elif bestmove == "quit":
                return "quit"
            else:
                print(f"[{self._text(self.name, self.color)}]: unknown command '{bestmove}'. Type help for more information.")

    def close(self):
        self.teacher.close()
        print(f"[{self._text('server','yellow')}]: closed [{self._text(self.name,self.color)}]")