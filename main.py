import pygame as pg
import random
from time import sleep, time
import PIL
import math
from chess_eval import evaluate_board

WIDTH = 800
HEIGHT = 800

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

pics = {
    WPAWN: pg.image.load('pics/white-pawn.png'),
    WROOK: pg.image.load('pics/white-rook.png'),
    WKNIGHT: pg.image.load('pics/white-knight.png'),
    WBISHOP: pg.image.load('pics/white-bishop.png'),
    WQUEEN: pg.image.load('pics/white-queen.png'),
    WKING: pg.image.load('pics/white-king.png'),
    BPAWN: pg.image.load('pics/black-pawn.png'),
    BROOK: pg.image.load('pics/black-rook.png'),
    BKNIGHT: pg.image.load('pics/black-knight.png'),
    BBISHOP: pg.image.load('pics/black-bishop.png'),
    BQUEEN: pg.image.load('pics/black-queen.png'),
    BKING: pg.image.load('pics/black-king.png'),
}

for p in pics:
    pics[p] = pg.transform.scale(pics[p], (100, 100))

COLOR1 = (200, 180, 140)
# COLOR2 = (150, 135, 105)
COLOR2 = (120, 108, 84)
SELECTCOLOR = (200, 200, 120)


class ChessGame:
    def __init__(self):
        self.board = self.make_board()
        self.turn = WHITE
        self.winner = EMPTY

        self.promote_pawn = False
        self.promote_pawn_loc = (-1, -1)
        self.promote_color = EMPTY

    # def evaluate_moves(self, turn, n=1):
    #     moves = []

    #     for r in range(0, len(self.board)):
    #         for c in range(0, len(self.board[r])):
    #             if self.what_color((r, c), self.board) == turn:
    #                 piece_moves = self.get_valid_moves((r, c), self.board)
    #                 for pm in piece_moves:
    #                     new_board = self.copy_board()
    #                     new_board.move((r, c), pm)
    #                     moves.append((evaluate_board(new_board.board), ((r, c), (pm[0], pm[1]))))

    #     if turn == WHITE:
    #         moves = sorted(moves, key=lambda x: x[0], reverse=True)
    #     elif turn == BLACK:
    #         moves = sorted(moves, key=lambda x: x[0], reverse=False)
        
    #     moves = moves[:(5 if len(moves) >= 5 else len(moves))]

    #     if n > 3:
    #         return moves[0][0]
    #     else:
    #         new_turn = WHITE if turn == BLACK else BLACK
    #         new_moves = []
    #         for rat, mv_ in moves:
    #             # print(rat, mv_)
    #             new_board = self.copy_board()
    #             new_board.move(mv_[0], mv_[1])
    #             new_moves.append((new_board.evaluate_moves(new_turn, n+1), mv_))
    #             if n == 1:
    #                 print(new_moves)
    #                 breakpoint()
            
    #         if new_turn == WHITE:
    #             new_moves = sorted(new_moves, key=lambda x: x[0], reverse=True)
    #         elif new_turn == BLACK:
    #             new_moves = sorted(new_moves, key=lambda x: x[0], reverse=False)

    #         if n == 1:
    #             r = new_moves[0][0]
    #             choose_moves = []
    #             for m in new_moves:
    #                 if m[0] == r:
    #                     choose_moves.append(m)
    #             return random.choice(choose_moves)


    #         return new_moves[0][0]


    def evaluate_moves_rec(self, turn):
        moves = []

        for r in range(0, len(self.board)):
            for c in range(0, len(self.board[r])):
                if self.what_color((r, c), self.board) == turn:
                    piece_moves = self.get_valid_moves((r, c))
                    for pm in piece_moves:
                        new_board = self.copy_board()
                        new_board.move((r, c), pm)
                        moves.append((evaluate_board(new_board), ((r, c), (pm[0], pm[1]))))

        random.shuffle(moves)

        if turn == WHITE:
            moves = sorted(moves, key=lambda x: x[0], reverse=True)
        elif turn == BLACK:
            moves = sorted(moves, key=lambda x: x[0], reverse=False)
        
        return moves
    

    def evaluate_moves(self, turn, n=1):
        moves = self.evaluate_moves_rec(self.turn)

        if n != -1:
            moves = moves[:(5 if len(moves) >= 5 else len(moves))]

        if len(moves) == 0:
            print('Checkmate found', n)
            if turn == WHITE:
                return (-100000, None)
            else:
                return (100000, None)
        
        if n > 3:
            return moves[0]
        else:
            new_turn = WHITE if self.turn == BLACK else BLACK
            new_moves = []
            for rating, move in moves:
                new_board = self.copy_board()
                new_board.move(move[0], move[1])
                to_add = 1
                if rating != evaluate_board(new_board):
                    to_add = 0
                new_moves.append( (new_board.evaluate_moves(new_turn, n+to_add)[0], move) )
                # print(rating, move, new_board.evaluate_moves(new_turn, n+1))
            if turn == WHITE:
                new_moves = sorted(new_moves, key=lambda x: x[0], reverse=True)
            elif turn == BLACK:
                new_moves = sorted(new_moves, key=lambda x: x[0], reverse=False)

            # new_moves = new_moves[:(5 if len(new_moves) >= 5 else len(new_moves))]
            r = new_moves[0][0]
            choose_moves = []
            for m in new_moves:
                if m[0] == r:
                    choose_moves.append(m)
            return random.choice(choose_moves)



    def copy_board(self):
        new_board = ChessGame()
        new_board.board = [r.copy() for r in self.board]
        new_board.turn = self.turn
        new_board.winner = self.winner
        new_board.promote_pawn = self.promote_pawn
        new_board.promote_pawn_loc = self.promote_pawn_loc
        new_board.promote_color = self.promote_color
        return new_board

    # def make_board(self):
    #     b = []

    #     b.append(
    #         [BROOK, BKNIGHT, BBISHOP, BQUEEN, BKING, BBISHOP, BKNIGHT, BROOK]
    #     )
    #     b.append(
    #         [BPAWN for i in range(0, 8)]
    #     )

    #     b = b + [[EMPTY for i in range(0, 8)] for i in range(0, 4)]

    #     b.append(
    #         [WPAWN for i in range(0, 8)]
    #     )
    #     b.append(
    #         [WROOK, WKNIGHT, WBISHOP, WQUEEN, WKING, WBISHOP, WKNIGHT, WROOK]
    #     )

    #     return b

    def make_board(self):
        return [[22, 0, 44, 55, 66, 44, 33, 22], [11, 11, 11, 0, 11, 11, 11, 11], [0, 0, 33, 0, 0, 0, 0, 0], [0, 0, 0, 11, 0, 0, 0, 0], [0, 0, 0, 1, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 1, 1, 1, 1], [2, 3, 0, 5, 6, 4, 3, 2]]
        # return [[22, 55, 66, 0, 5, 44, 33, 22], [11, 11, 11, 0, 0, 11, 11, 11], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1, 1], [0, 2, 0, 0, 6, 4, 3, 2]]

    def what_color(self, pos, board):
        piece = board[pos[0]][pos[1]]
        if piece == EMPTY:
            return EMPTY
        elif piece > 10:
            return BLACK
        else:
            return WHITE

    def get_rook_moves(self, pos, color, board):
        r, c = pos
        mvs = []
        # Left
        c_ = c-1
        while c_ >= 0:
            pc = self.what_color((r, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r, c_))
                break
            mvs.append((r, c_))
            c_ -= 1
        # Right
        c_ = c+1
        while c_ <= 7:
            pc = self.what_color((r, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r, c_))
                break
            mvs.append((r, c_))
            c_ += 1
        # Up
        r_ = r-1
        while r_ >= 0:
            pc = self.what_color((r_, c), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c))
                break
            mvs.append((r_, c))
            r_ -= 1
        # Down
        r_ = r+1
        while r_ <= 7:
            pc = self.what_color((r_, c), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c))
                break
            mvs.append((r_, c))
            r_ += 1
        
        return mvs

    def get_bishop_moves(self, pos, color, board):
        r, c = pos
        mvs = []
        # Top Left
        r_ = r-1
        c_ = c-1
        while 0 <= r_ <= 7 and 0 <= c_ <= 7:
            pc = self.what_color((r_, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c_))
                break
            mvs.append((r_, c_))
            c_ -= 1
            r_ -= 1
        # Top Right
        r_ = r-1
        c_ = c+1
        while 0 <= r_ <= 7 and 0 <= c_ <= 7:
            pc = self.what_color((r_, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c_))
                break
            mvs.append((r_, c_))
            c_ += 1
            r_ -= 1
        # Bottom Right
        r_ = r+1
        c_ = c+1
        while 0 <= r_ <= 7 and 0 <= c_ <= 7:
            pc = self.what_color((r_, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c_))
                break
            mvs.append((r_, c_))
            c_ += 1
            r_ += 1
        # Bottom Left
        r_ = r+1
        c_ = c-1
        while 0 <= r_ <= 7 and 0 <= c_ <= 7:
            pc = self.what_color((r_, c_), board)
            if pc != EMPTY:
                if pc != color:
                    mvs.append((r_, c_))
                break
            mvs.append((r_, c_))
            c_ -= 1
            r_ += 1


        return mvs

    def get_knight_moves(self, pos, color, board):
        r, c = pos
        mvs = []
        mvs_tt = [ (r-2, c+1), (r-2, c-1), (r+2, c+1), (r+2, c-1), (r+1, c+2), (r-1, c+2), (r+1, c-2), (r-1, c-2) ]
        for mv in mvs_tt:
            if 0 <= mv[0] <= 7 and 0 <= mv[1] <= 7:
                pc = self.what_color(mv, board)
                if pc != color:
                    mvs.append(mv)
        return mvs

    def get_king_moves(self, pos, color, board):
        r, c = pos
        mvs = []

        mvs_tt = [(r-1, c_) for c_ in range(c-1, c+2)] + [(r+1, c_) for c_ in range(c-1, c+2)] + [(r, c-1), (r, c+1)]
        for mv in mvs_tt:
            if 0 <= mv[0] <= 7 and 0 <= mv[1] <= 7:
                pc = self.what_color(mv, board)
                if pc != color:
                    temp_board = [ro.copy() for ro in board]
                    temp_board[r][c] = EMPTY
                    temp_board[mv[0]][mv[1]] = board[r][c] + 0
                    if not self.check_check(mv, color, temp_board)[0]:
                        mvs.append(mv)
        
        return mvs

    def check_check(self, pos, color, board):
        r, c = pos

        # Vertical
        # Up
        r_ = r-1
        c_ = c+0
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WROOK or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ -= 1
        # Down
        r_ = r+1
        c_ = c+0
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WROOK or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ += 1

        # Horizontal
        # Left
        r_ = r+0
        c_ = c-1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WROOK or piece == WQUEEN:
                        return True, (r_, c_)
                break
            c_ -= 1
        # Right
        r_ = r+0
        c_ = c+1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WROOK or piece == WQUEEN:
                        return True, (r_, c_)
                break
            c_ += 1
        

        # Diagonal

        # Top Left
        r_ = r-1
        c_ = c-1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WBISHOP or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ -= 1
            c_ -= 1
        
        # Top Right
        r_ = r-1
        c_ = c+1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            piece = board[r_][c_]
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WBISHOP or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ -= 1
            c_ += 1
        
        # Bottom Left
        r_ = r+1
        c_ = c-1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WBISHOP or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ += 1
            c_ -= 1
        
        # Bottom Right
        r_ = r+1
        c_ = c+1
        while 7 >= c_ >= 0 and 7 >= r_ >= 0:
            col = self.what_color((r_, c_), board)
            if col != EMPTY:
                if col != color:
                    piece = int(str(board[r_][c_])[:1])
                    if piece == WBISHOP or piece == WQUEEN:
                        return True, (r_, c_)
                break
            r_ += 1
            c_ += 1

        kmvs_tt = [ (r-2, c+1), (r-2, c-1), (r+2, c+1), (r+2, c-1), (r+1, c+2), (r-1, c+2), (r+1, c-2), (r-1, c-2) ]
        kingmvs_tt = [(r-1, c_) for c_ in range(c-1, c+2)] + [(r+1, c_) for c_ in range(c-1, c+2)] + [(r, c-1), (r, c+1)]
        if color == WHITE:
            if r > 0:
                if c > 0 and board[r-1][c-1] == BPAWN:
                    return True, (r-1, c-1)
                if c < 7 and board[r-1][c+1] == BPAWN:
                    return True, (r-1, c+1)
            for m in kmvs_tt:
                if 7 >= m[0] >= 0 and 7 >= m[1] >= 0:
                    if board[m[0]][m[1]] == BKNIGHT:
                        return True, m
            for m in kingmvs_tt:
                if 7 >= m[0] >= 0 and 7 >= m[1] >= 0:
                    if board[m[0]][m[1]] == BKING:
                        return True, m
        else:
            if r < 7:
                if c > 0 and board[r+1][c-1] == WPAWN:
                    return True, (r+1, c-1)
                if c < 7 and board[r+1][c+1] == WPAWN:
                    return True, (r+1, c+1)
            for m in kmvs_tt:
                if 7 >= m[0] >= 0 and 7 >= m[1] >= 0:
                    if board[m[0]][m[1]] == WKNIGHT:
                        return True, m
            for m in kingmvs_tt:
                if 7 >= m[0] >= 0 and 7 >= m[1] >= 0:
                    if board[m[0]][m[1]] == WKING:
                        return True, m

        return False, (-1, -1)

    def get_valid_moves(self, pos):
        r, c = pos
        piece = self.board[r][c]
        color = self.what_color(pos, self.board)
        mvs = []
        if piece == WPAWN:
            if r == 0:
                pass  # TODO Upgrade Piece
            else:
                mvs = []
                if self.board[r-1][c] == EMPTY:
                    mvs.append((r-1, c))
                    if r == 6 and self.board[r-2][c] == EMPTY:
                        mvs.append( (r-2, c) )
                if c > 0 and EMPTY != self.what_color((r-1, c-1), self.board) != color:
                    mvs.append((r-1, c-1))
                if c < 7 and EMPTY != self.what_color((r-1, c+1), self.board) != color:
                    mvs.append((r-1, c+1))
        elif piece == BPAWN:
            if r == 7:
                pass  # TODO Upgrade Piece
            else:
                mvs = []
                if self.board[r+1][c] == EMPTY:
                    mvs.append((r+1, c))
                    if r == 1 and self.board[r+2][c] == EMPTY:
                        mvs.append( (r+2, c) )
                if c > 0 and EMPTY != self.what_color((r+1, c-1), self.board) != color:
                    mvs.append((r+1, c-1))
                if c < 7 and EMPTY != self.what_color((r+1, c+1), self.board) != color:
                    mvs.append((r+1, c+1))
        elif piece == WROOK or piece == BROOK:
            mvs = self.get_rook_moves(pos, color, self.board)
        elif piece == WBISHOP or piece == BBISHOP:
            mvs = self.get_bishop_moves(pos, color, self.board)
        elif piece == WKNIGHT or piece == BKNIGHT:
            mvs = self.get_knight_moves(pos, color, self.board)
        elif piece == WQUEEN or piece == BQUEEN:
            mvs = self.get_rook_moves(pos, color, self.board) + self.get_bishop_moves(pos, color, self.board)
        if piece == WKING or piece == BKING:
            new_mvs = self.get_king_moves(pos, color, self.board)
        else:
            king_loc = self.get_king_loc(color, self.board)
            new_mvs = []
            for mv in mvs:
                temp_board = [ro.copy() for ro in self.board]
                temp_board[r][c] = EMPTY
                temp_board[mv[0]][mv[1]] = self.board[r][c] + 0
                if not self.check_check(king_loc, color, temp_board)[0]:
                    new_mvs.append(mv)

        return new_mvs

    def in_check_mate(self, color, board):
        king_loc = self.get_king_loc(color, board)
        move_exists = False
        in_check, check_loc = self.check_check(king_loc, color, board)
        if in_check:
            if len(self.get_valid_moves(king_loc)) == 0:
                block_squares = []
                # What squares block
                r_, c_ = check_loc
                r_int = 0
                c_int = 0

                if r_ > king_loc[0]:
                    r_int = -1
                elif r_ < king_loc[0]:
                    r_int = 1
                if c_ > king_loc[1]:
                    c_int = -1
                elif c_ < king_loc[1]:
                    c_int = 1

                rh_limit = king_loc[0] if r_int >= 0 else 7
                rl_limit = king_loc[0] if r_int < 0 else 0

                ch_limit = king_loc[1] if c_int >= 0 else 7
                cl_limit = king_loc[1] if c_int < 0 else 0

                while rh_limit >= r_ >= rl_limit and ch_limit >= c_ >= cl_limit and (r_ != king_loc[0] and c_ != king_loc[1]):
                    block_squares.append((r_, c_))
                    r_ += r_int
                    c_ += c_int


                for r in range(0, len(board)):
                    if not move_exists:
                        for c in range(0, len(board[r])):
                            if r == 6 and c == 6:
                                if self.what_color((r, c), board) == color:  # and WKING != board[r][c] != BKING:
                                    # print(self.get_valid_moves((r, c), board))
                                    for mv in self.get_valid_moves((r, c)):
                                        if mv in block_squares:
                                            move_exists = True
                                            break
                    else:
                        break
            else:
                move_exists = True
        else:
            move_exists = True

        if move_exists:
            return False
        return True

    def get_king_loc(self, color, board):
        king_loc = (-1, -1)
        for r_ in range(0, len(board)):
            for c_ in range(0, len(board)):
                if (board[r_][c_] == WKING or board[r_][c_] == BKING) and self.what_color((r_, c_), board) == color:
                    king_loc = (r_, c_)
                    break
        return king_loc

    def move(self, piece, new_loc):
        if new_loc in self.get_valid_moves(piece):
            piece_p = self.board[piece[0]][piece[1]]
            self.board[new_loc[0]][new_loc[1]] = self.board[piece[0]][piece[1]]
            self.board[piece[0]][piece[1]] = EMPTY
            pre_turn = self.turn + 0

            if self.turn == WHITE:
                self.turn = BLACK
            else:
                self.turn = WHITE
            if self.in_check_mate(self.turn, self.board):
                self.winner = pre_turn
            else:
                if (piece_p == WPAWN and new_loc[0] == 0) or (piece_p == BPAWN and new_loc[0] == 7):
                    self.promote_pawn = True
                    self.promote_pawn_loc = new_loc
                    self.promote_color = pre_turn + 0

                    self.promote_pawn_func((3, 3), self.board)
            if not self.promote_pawn:
                # print(f'Board Evaluation: {evaluate_board(self.board)}')
                pass
            return True
        return False

    def promote_pawn_func(self, choice_loc, board):
        piece = EMPTY
        if choice_loc[1] == 3:
            if choice_loc[0] == 3:
                piece = WQUEEN
            elif choice_loc[0] == 4:
                piece = WROOK
            else:
                return False
        elif choice_loc[1] == 4:
            if choice_loc[0] == 3:
                piece = WKNIGHT
            elif choice_loc[0] == 4:
                piece = WBISHOP
            else:
                return False
        else:
            return False
        
        if self.promote_color == BLACK:
            piece = int(str(piece) + str(piece))
        
        board[self.promote_pawn_loc[0]][self.promote_pawn_loc[1]] = piece
        self.promote_pawn = False
        # print(f'Board Evaluation: {evaluate_board(board)}')
        return True




class Player:
    def __init__(self, cg=ChessGame()):
        pg.init()

        self.cg = cg
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.box_size = WIDTH/8

        self.selected_piece = (-1, -1)

    def draw_board(self, screen):
        screen.fill(COLOR1)

        board = self.cg.board

        for r in range(0, len(board)):
            for c in range(0, len(board[r])):
                if self.selected_piece[0] == r and self.selected_piece[1] == c:
                    pg.draw.rect(screen, SELECTCOLOR, (c * self.box_size, r * self.box_size, self.box_size, self.box_size))
                elif (r + c) % 2 == 0:
                    pg.draw.rect(screen, COLOR1, (c * self.box_size, r * self.box_size, self.box_size, self.box_size))
                else:
                    pg.draw.rect(screen, COLOR2, (c * self.box_size, r * self.box_size, self.box_size, self.box_size))
                if board[r][c] != EMPTY:
                    screen.blit(pics[board[r][c]], (c * self.box_size, r * self.box_size, self.box_size, self.box_size))
        
        if self.selected_piece[0] != -1:
            mvs = self.cg.get_valid_moves(self.selected_piece)
            for mv in mvs:
                pg.draw.circle(screen, (50, 50, 50), ( mv[1] * self.box_size + self.box_size/2, mv[0] * self.box_size + self.box_size/2 ), 15)


        if self.cg.promote_pawn:
            cover = pg.Surface((WIDTH, HEIGHT))
            cover.set_alpha(150)
            cover.fill((50, 50, 50))
            screen.blit(cover, (0, 0))

            cover = pg.Surface((self.box_size*2, self.box_size*2))
            cover.set_alpha(215)
            cover.fill((50, 50, 50))
            screen.blit(cover, (self.box_size * 3, self.box_size * 3))
            
            if self.cg.promote_color == WHITE:
                screen.blit(pics[WQUEEN], (3 * self.box_size, 3 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[WROOK], (3 * self.box_size, 4 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[WKNIGHT], (4 * self.box_size, 3 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[WBISHOP], (4 * self.box_size, 4 * self.box_size, self.box_size, self.box_size))
            else:
                screen.blit(pics[BQUEEN], (3 * self.box_size, 3 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[BROOK], (3 * self.box_size, 4 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[BKNIGHT], (4 * self.box_size, 3 * self.box_size, self.box_size, self.box_size))
                screen.blit(pics[BBISHOP], (4 * self.box_size, 4 * self.box_size, self.box_size, self.box_size))
        

        pg.display.flip()

    def what_color(self, pos):
        piece = self.cg.board[pos[0]][pos[1]]
        if piece == EMPTY:
            return EMPTY
        elif piece > 10:
            return BLACK
        else:
            return WHITE
        
    def loop(self):
        self.running = True
        lm = time()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    row = math.floor(y / self.box_size)
                    col = math.floor(x / self.box_size)
                    if self.cg.promote_pawn:
                        self.cg.promote_pawn_func((row, col), self.cg.board)
                    else:
                        if self.what_color((row, col)) == self.cg.turn:
                            if self.selected_piece[0] == row and self.selected_piece[1] == col:
                                self.selected_piece = (-1, -1)
                            else:
                                self.selected_piece = (row, col)
                        else:
                            if self.selected_piece[0] == -1:
                                pass
                            else:
                                self.cg.move(self.selected_piece, (row, col))
                                self.selected_piece = (-1, -1)
                                if self.cg.winner != EMPTY:
                                    print(num_to_word[self.cg.winner], 'wins')
                                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHTBRACKET:
                        mv = self.cg.evaluate_moves(self.cg.turn)
                        print('mv', mv)
                        self.cg.move(mv[1][0], mv[1][1])
                        # self.cg.move(mv[1][0], mv[1][1])
            
            self.draw_board(self.screen)

        


def main():
    p = Player()
    p.loop()
    


main()













