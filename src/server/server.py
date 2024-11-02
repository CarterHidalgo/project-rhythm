# Name: server.py
# Author: Carter Hidalgo
#
# Purpose: send and receive uci commands with two players (either human or chess engine)

import time
from helper.board import Board
from server.engine import Engine
from server.human import Human
from helper.colors import yellow, purple
from helper.paths import berserk_path, obsidian_path

class Server:
    def __init__(self, player_one, player_two):

        self.engines = [
            ["berserk", berserk_path],
            ["obsidian", obsidian_path],
        ]
        self.init = False
        self.show_help = False

        if(player_one == "cpu"):
            self.eng_one = Engine(self.engines[0][1], self.engines[0][0], "green", False)
            self.eng_one.send_and_wait("uci", Engine.UCIOK)
            self.eng_one.isready_wait()
        else:
            self.eng_one = Human("player one", "green")

        if(player_two == "cpu"):
            self.eng_two = Engine(self.engines[1][1], self.engines[1][0], "cyan", False)
            self.eng_two.send_and_wait("uci", Engine.UCIOK)
            self.eng_two.isready_wait()
        else:
            self.eng_two = Human("player two", "cyan")

        self.eng_curr = self.eng_one
        self.init = True

    def is_init(self):
        return self.init
    
    def get_bestmove(self):
        if isinstance(self.eng_curr, Engine):
            cmd = "position fen " + Board.get_start_fen()
            if(Board.moves):
                cmd += " moves "
                for move in Board.moves:
                    cmd += move + " "
            self.eng_curr.send(cmd)

            cmd = "go" + " wtime " + str(Board.go_params[0]) + " btime " + str(Board.go_params[1])
        else:
            cmd = ""
            if not self.show_help:
                self.show_help = True
                print(f"[{yellow('server')}]: waiting for player input; type 'help' for more")

        start_time = time.time()
        bestmove = self.eng_curr.send_and_wait(cmd, Engine.BESTMOVE)
        total_time = (time.time() - start_time) * 1000

        if bestmove == "quit":
            return bestmove

        self.eng_curr.sub_time(total_time)

        Board.add_move(bestmove)    
        Board.set_go_params((self.eng_one.get_time(), self.eng_two.get_time()))
        
        print(f"[{yellow('server')}] -> [{purple('controller')}]: {bestmove}")

        return bestmove
    
    def flip_curr_eng(self):
        if self.eng_curr == self.eng_one:
            self.eng_curr = self.eng_two
        elif self.eng_curr == self.eng_two:
            self.eng_curr = self.eng_one

    def close(self):
        self.eng_one.close()
        self.eng_two.close()
        print(f"[{yellow('server')}]: closed [{yellow('server')}]")


