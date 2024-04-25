import random
import math


WHITE = 1
BLACK = 2

num_to_word = {
    WHITE: 'WHITE',
    BLACK: 'BLACK'
}


EMPTY = 0
WPAWN = 1
WROOK = 2
WKNIGHT = 3
WBISHOP = 4
WQUEEN = 5
WKING = 6

BPAWN = 11
BROOK = 22
BKNIGHT = 33
BBISHOP = 44
BQUEEN = 55
BKING = 66


values_conv = {
    WPAWN: 124,
    WKNIGHT: 781,
    WBISHOP: 825,
    WROOK: 1276,
    WQUEEN: 2538,
    WKING: 0,

    BPAWN: -124,
    BKNIGHT: -781,
    BBISHOP: -825,
    BROOK: -1276,
    BQUEEN: -2538,
    BKING: 0,
    
    EMPTY: 0,
}


def evaluate_board(cg):
    score = 0
    score += middle_game(cg)
    return score

def middle_game(cg):
    score = 0
    score += piece_value(cg.board)
    # score += pieces_attacked(cg)
    return score

def piece_value(board):
    score = 0
    for r in board:
        for c in r:
            score += values_conv[c]
    return score

def pieces_attacked(cg):
    pieces_attacked = []
    for r in range(0, len(cg.board)):
        for c in range(0, len(cg.board[r])):
            piece_color = what_color((r, c), cg.board)
            valid_moves = cg.get_valid_moves((r, c))
            for m in valid_moves:
                temp_piece_color = what_color(m, cg.board)
                if EMPTY != temp_piece_color != piece_color:
                    pieces_attacked.append(m)
    score = 0
    for p in pieces_attacked:
        score += values_conv[ cg.board[p[0]][p[1]] ] / 8
    return score










def what_color(pos, board):
    piece = board[pos[0]][pos[1]]
    if piece == EMPTY:
        return EMPTY
    elif piece > 10:
        return BLACK
    else:
        return WHITE












