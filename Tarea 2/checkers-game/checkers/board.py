import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        # print ("EVALUATE")
        # print ("white left:", self.white_left)
        # print ("red left:", self. red_left)
        # print ("white kings:", self.white_kings)
        # print ("red_kings:", self.red_kings)
        # print ("value is: ", self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5))
        # print ("-------------------------------------------------------------------")
        
                # print(self.board[row][col], end=", ")
            #print ("\n")
        # print ("-------------------------------------------------------------------")        
        evaluation = self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5) 
        return evaluation

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 or row == 0) and not piece.king:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            print ("I will remove a piece!")
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                    if piece.king == True:
                        self.red_kings -= 1
                else:
                    self.white_left -= 1
                    if piece.king == True:
                        self.white_kings -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(piece.king, row -1, max(row-3, -1), -1, piece.color, left, 1))
            moves.update(self._traverse_right(piece.king, row -1, max(row-3, -1), -1, piece.color, right, 1))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(piece.king, row +1, min(row+3, ROWS), 1, piece.color, left, 1))
            moves.update(self._traverse_right(piece.king, row +1, min(row+3, ROWS), 1, piece.color, right, 1))

        print ("moves are:")
        print (moves)
    
        return moves

    def _traverse_left(self, is_king, start, stop, step, color, left, iteracion, skipped=[]):
        print ("---------------------------------------------------------")
        print ("TRAVERSE LEFT, iteracion:", iteracion)
        moves = {}
        last = []
        print ("start, stop, step: ")
        print (start, stop, step)
        # print ("left", left)
        if start >= ROWS or start < 0:
            print ("start is", start, "then return no moves")
            return moves
        for r in range(start, stop, step):
            print ("r is:", r)
            if left < 0:
                print ("LEFT < 0")
                break
            if r >= ROWS or r < 0:
                print ("r>=ROWS or r<0")
                break
            
            current = self.board[r][left]
            print ("current is: ", current)
            if current == 0:
                print ("current is equal to 0")
                if skipped and not last:
                    print ("skipped and not last, then break")
                    break
                elif skipped:
                    print ("skipped and there is a last")
                    print ("skipped:", skipped)
                    print ("last:", last)
                    moves[(r, left)] = last + skipped
                    print (moves[(r, left)])
                else:
                    print ("not skipped, just else bro")
                    moves[(r, left)] = last
                    print (moves[(r, left)])
                
                if last:
                    print ("existe last, esto significa que comí una pieza")
                    if step == -1:
                        row = max(r-3, -1)
                        row_king = min(r+3, ROWS+1) 
                    else:
                        row = min(r+3, ROWS+1)
                        row_king = max(r-3, -1)
                    moves.update(self._traverse_left(is_king, r+step, row, step, color, left-1, iteracion+1, skipped=skipped+last))
                    moves.update(self._traverse_right(is_king, r+step, row, step, color, left+1, iteracion+1, skipped=skipped+last))
                    if is_king:
                        print ("soy king, puedo ir al revés")
                        moves.update(self._traverse_left(is_king, r-step, row_king, -step, color, left-1, iteracion+1, skipped=skipped+last))

                break
            elif current.color == color:
                print ("current.color equals to color: ", color, ", then break")
                break
            else:
                last = [current]
                print ("last ha sido asignado a current: ", current.row, ",", current.col)

            left -= 1
        
        return moves

    def _traverse_right(self, is_king, start, stop, step, color, right, iteracion, skipped=[]):
        print ("---------------------------------------------------------")
        print ("TRAVERSE RIGHT, iteracion:", iteracion)
        moves = {}
        last = []
        print ("start, stop, step: ")
        print (start, stop, step)
        if start >= ROWS or start < 0:
            print ("start is", start, "then return no moves")
            return moves
        for r in range(start, stop, step):
            print ("r is:", r)
            if right >= COLS:
                print ("RIGHT >= COLS")
                break
            if r >= ROWS or r < 0:
                print ("r>=ROWS or r<0")
                break
            
            current = self.board[r][right]
            if current == 0:
                print ("current is equal to 0")
                if skipped and not last:
                    print ("skipped and not last, then break")
                    break
                elif skipped:
                    print ("skipped and there is a last")
                    print ("skipped:", skipped)
                    print ("last:", last)
                    moves[(r,right)] = last + skipped
                    print (moves[(r,right)]) 
                else:
                    print ("not skipped, just else bro")
                    moves[(r, right)] = last
                    print (moves[(r,right)] )
                
                if last:
                    print ("existe last, esto significa que comí una pieza")
                    if step == -1:
                        row = max(r-3, -1)
                        row_king = min(r+3, ROWS+1)
                    else:
                        row = min(r+3, ROWS+1)
                        row_king = max(r-3, -1)
                    moves.update(self._traverse_left(is_king, r+step, row, step, color, right-1, iteracion+1, skipped=skipped+last))
                    moves.update(self._traverse_right(is_king, r+step, row, step, color, right+1, iteracion+1, skipped=skipped+last))
                    if is_king:
                        print ("soy king, puedo ir al revés")
                        moves.update(self._traverse_right(is_king, r-step, row_king, -step, color, right+1, iteracion+1, skipped=skipped+last))
                        
                break
            elif current.color == color:
                print ("current.color equals to color: ", color, ", then break")
                break
            else:
                last = [current]
                print ("last ha sido asignado a current: ", current.row, current.col)

            right += 1
        
        return moves
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces