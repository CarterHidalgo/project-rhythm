# Name: manager.py
# Author: Carter Hidalgo
#
# Purpose: manage messages between the scara and the controller

import queue, time
from frontend.client import Client
from frontend.board import Board
from frontend.move import *
from colors.colors import pink, purple

class Manager:
    def __init__(self):
        self.tasks = queue.Queue()

    def _print(self, text):
        if text:
            print(f"[{pink('scara')}]: {text}")

    def _quiet_move(self, fromIndex, toIndex):
        self.tasks.put(("move", fromIndex))
        self.tasks.put(("height", Board.get(fromIndex).lower()))
        self.tasks.put(("grab", None))
        self.tasks.put(("height", "h"))
        self.tasks.put(("move", toIndex))
        self.tasks.put(("height", Board.get(fromIndex).lower()))
        self.tasks.put(("release", None))
        self.tasks.put(("height", "h"))

    def _remove_piece(self, index):
        type = Board.get(index)
        sideline = Board.get_cap(type)

        self.tasks.put(("move", index))
        self.tasks.put(("height", Board.get(index).lower()))
        self.tasks.put(("grab", None))
        self.tasks.put(("height", "h"))
        self.tasks.put(("move", sideline))
        self.tasks.put(("height", Board.get(index).lower()))
        self.tasks.put(("release", None))
        self.tasks.put(("height", "h"))

    def move_to_tasks(self, move):
        fromIndex, toIndex, promo = Board.parse_move(move)
        type = Board.get(fromIndex)

        if is_promo(move):
            if is_capture(move):
                self._remove_piece(toIndex)
            self._remove_piece(fromIndex)
            # move promoted piece onto the board
            
            return self.tasks
        elif is_king_castle(move):
            self._print("move kingside rook")
        elif is_queen_castle(move):
            self._print("move rook queenside")
        elif is_en_passant(move):
            if type.isupper():
                self._remove_piece(toIndex - 8)
            else:
                self._remove_piece(toIndex + 8)
        elif is_capture(move):
            self._remove_piece(toIndex)
        self._quiet_move(fromIndex, toIndex)

    def send_move_wait(self, move):
        self.tasks.queue.clear()
        self.move_to_tasks(move)

        Client.send_data(self.tasks)

        while(Client.is_waiting()):
            time.sleep(1)
        
        return move
    
    # def close(self):
