# Name: board.py
# Author: Carter Hidalgo
#
# Purpose: store a full stateless representation of the board

from colors.colors import blue, red, yellow

class Board:
    play_time = 300000
    board = [None] * 64
    go_params = [play_time, play_time]
    moves = []
    wcap = -1
    bcap = 64
    start_fen = ""

    def __init__(go_params):
        print("\n\n\nreached")
        Board.go_params = go_params

    def get_start_fen():
        return Board.start_fen

    def get_turn():
        return Board.turn
    
    def next_turn():
        Board.turn = not Board.turn

    def set_go_params(go_params):
        Board.go_params = go_params

    def add_move(move):
        Board.moves.append(move)

    def add_cap(type):
        if type.isupper():
            wcap -= 1
        else:
            bcap += 1

    def get_cap(type):
        if type.isupper():
            return Board.wcap
        else:
            return Board.bcap

    def set(index, value):
        Board.board[index] = value

    def get(index):
        return Board.board[index]
    
    def parse_move(move):
        rank = int(move[1:2]) - 1
        file = ord(move[0:1]) - 97
        fromIndex = rank * 8 + file

        rank = int(move[3:4]) - 1
        file = ord(move[2:3]) - 97
        toIndex = rank * 8 + file

        if len(move) > 4:
            promo = move[4:5]
        else:
            promo = ""

        return fromIndex, toIndex, promo
    
    def is_occupied(index):
        return Board.board[index] != "";

    def set_with_fen(fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        rank = 7
        file = 0

        Board.start_fen = fen
        Board.board.clear

        for c in fen:
            if(c == ' '):
                break;
            elif(c == '/'):
                rank -= 1
                file = 0;
            elif(c.isdigit()):
                num_empty = int(c)

                for i in range(num_empty):
                    Board.board[rank * 8 + file] = "";
                    file += 1
            else:
                Board.board[rank * 8 + file] = c;
                file += 1
    
    def print():
        index = 0

        print(f"[{yellow('server')}]: printing board")
        print("\n   a b c d e f g h\n");

        for i in range(8, 0, -1):
            print(f"{i} ", end="");

            for j in range(8):
                index = (i-1) * 8 + j

                print(" ", end="")

                if(Board.board[index].isupper()):
                    print(blue(Board.board[index]), end="")
                elif(Board.board[index].islower()):
                    print(red(Board.board[index]), end="")
                else:
                    print(".", end="");
            print(f"  {i}")

        print("\n   a b c d e f g h\n")