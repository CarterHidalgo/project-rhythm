# Name: move.py
# Author: Carter Hidalgo
#
# Purpose: provide methods for understanding the properties of a move in algebraic notation e.g. "e2e4"

from helper.board import Board

def is_capture(move):
    fromIndex, toIndex, promo = Board.parse_move(move)
    return Board.get(toIndex) != ""

def is_en_passant(move):
    fromIndex, toIndex, promo = Board.parse_move(move)
    type = Board.get(fromIndex)

    if type.lower() != "p":
        return False
    if abs(fromIndex - toIndex) != 7 and abs(fromIndex - toIndex) != 9:
        return False
    if Board.get(toIndex) != "":
        return False
    return True

def is_king_castle(move):
    fromIndex, toIndex, promo = Board.parse_move(move)
    type = Board.get(fromIndex)

    if type.lower() != "k":
        return False
    if abs(fromIndex - toIndex) != 2:
        return False
    if fromIndex < toIndex:
        return False
    else:
        return True

def is_queen_castle(move):
    fromIndex, toIndex, promo = Board.parse_move(move)
    type = Board.get(fromIndex)

    if type.lower() != "k":
        return False
    if abs(fromIndex - toIndex) != 2:
        return False
    if fromIndex > toIndex:
        return False
    else:
        return True

def is_promo(move):
    fromIndex, toIndex, promo = Board.parse_move(move)

    return promo != ""

def make_move(move):
    fromIndex, toIndex, promo = Board.parse_move(move)

    if is_promo(move):
        Board.board[fromIndex] = ""
        Board.board[toIndex] = promo
    elif is_king_castle(move):
        Board.board[fromIndex + 1] = Board.board[fromIndex + 3]
        Board.board[fromIndex + 3] = ""
        Board.board[toIndex] = Board.board[fromIndex]
        Board.board[fromIndex] = ""
    elif is_queen_castle(move):
        Board.board[fromIndex - 1] = Board.board[fromIndex - 4]
        Board.board[fromIndex - 4] = ""
        Board.board[toIndex] = Board.board[fromIndex]
        Board.board[fromIndex] = ""
    elif is_en_passant(move):
        if Board.get(fromIndex).isupper():
            Board.board[toIndex + 8] = ""
        else:
            Board.board[toIndex - 8] = ""
        Board.board[toIndex] = Board.board[fromIndex]
        Board.board[fromIndex] = ""
    else:
        Board.board[toIndex] = Board.board[fromIndex]
        Board.board[fromIndex] = ""
