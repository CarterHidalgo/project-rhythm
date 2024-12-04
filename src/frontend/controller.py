# Name: controller.py
# Author: Carter Hidalgo
#
# Purpose: pass control and communication between server and scara loops and update board representation

from frontend.server import Server
from frontend.manager import Manager
from frontend.board import Board
from frontend.move import make_move
from colors.colors import purple, pink

class Controller:
    INIT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    INIT = False

    def _get_players(self):
        player_one = ""
        player_two = ""
        print(f"[{purple('controller')}]: loaded")
        
        while player_one != "human" and player_one != "cpu":
            print(f"[{purple('controller')}]: selection for player one choose [\"human\",\"cpu\"]: ", end="")
            player_one = input()
            if(player_one == "quit"):
                return "quit", "quit"
        while player_two != "human" and player_two != "cpu":
            print(f"[{purple('controller')}]: selection for player two choose [\"human\",\"cpu\"]: ", end="")
            player_two = input()
            if(player_two == "quit"):
                return "quit", "quit"

        return player_one, player_two


    def __init__(self):
        self.running = True
        Board.set_with_fen(Controller.INIT_FEN)

        player_one, player_two = self._get_players()
        if(player_one == "quit" or player_two == "quit"):
            self.running = False
            return

        self.message = ""
        self.turn = "server"
        self.server = Server(player_one, player_two)
        self.manager = Manager()
        Controller.INIT = True

    def is_running(self):
        return self.running

    def run(self):
        while(self.turn == "server"):
            if(self.server.is_init()):
                self.message = self.server.get_bestmove()
                if self.message == "quit":
                    self.running = False
                    break
                self.server.flip_curr_eng()
                self.turn = "scara"

                print(f"[{purple('controller')}] -> [{pink('scara')}]: {self.message}")

        while(self.turn == "scara"):
            self.manager.send_move_wait(self.message)
            make_move(self.message)
            Board.print()
            self.turn = "server"

    def close(self):
        print()
        if Controller.INIT:
            self.server.close()
        # if self.manager:
        #     self.manager.close()
        self.running = False
        print(f"[{purple('controller')}]: closed")