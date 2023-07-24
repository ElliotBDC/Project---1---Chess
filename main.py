import pygame
import time
from copy import deepcopy
import ai 
import threading

# Declaring colours in binary format

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (118,150,86)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

BACKGROUND_COLOUR_1 = hex_to_rgb('#262626')
#BACKGROUND_COLOUR_1 = hex_to_rgb('#272932')
BBLUE = hex_to_rgb('#75b6c6')
NEW = hex_to_rgb('#114b5f')

# Setting up the screen, etc via Pygame

pygame.init()

screen_size = pygame.display.Info()
screen_width = screen_size.current_w
screen_height = screen_size.current_h
current_size = (screen_width*0.5,  screen_height*0.5)
screen = pygame.display.set_mode(current_size)
pygame.display.set_caption("Chess")
done = False
clock = pygame.time.Clock()

# Loading images of the chess pieces

"""
wp = [colour, piece]
e.g wp = [white, pawn] hence -> wp
"""

wp = pygame.image.load("images/wp.png")
wr = pygame.image.load("images/wr.png")
wb = pygame.image.load("images/wb.png")
wn = pygame.image.load("images/wn.png")
wq = pygame.image.load("images/wq.png")
wk = pygame.image.load("images/wk.png")
bp = pygame.image.load("images/bp.png")
bq = pygame.image.load("images/bq.png")
br = pygame.image.load("images/br.png")
bn = pygame.image.load("images/bn.png")
bb = pygame.image.load("images/bb.png")
bk = pygame.image.load("images/bk.png")
pygame.display.set_icon(bp)

images = [
    ['wp', wp],
    ['wr', wr],
    ['wb', wb],
    ['wn', wn],
    ['wq', wq],
    ['wk', wk],
    ['bp', bp],
    ['bq', bq],
    ['br', br],
    ['bn', bn],
    ['bb', bb],
    ['bk', bk]
]
classic_board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]


# Formats the time in seconds to a minutes:seconds representation

def secondsToTime(seconds):
    minutes = seconds // 60
    secondsLeft = seconds - (minutes*60)
    if minutes < 10:
        minutes = "0" + str(minutes)
    if secondsLeft < 10:
        secondsLeft = "0" + str(secondsLeft)
    return (f"{minutes}:{secondsLeft}")

# Variable used when pawn is promoted and player needs to choose replacing piece

choice_making = False

# Declaring the class for the chess board (functionality & design)

class Board():
    # Display Properties
    board_x = current_size[0]*0.05
    board_y = 0.15*current_size[1]
    board_height = current_size[1]*0.7
    board_width = board_height
    box_dimen = (current_size[1]*0.7) // 8

    #Board 
    move = 0
    white_king = [7, 4]
    black_king = [0, 4]
    board = [
    ['', '', '', '', 'bk', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', 'wr', ''],
    ['', '', '', '', '', '', 'wr', ''],
    ['', '', '', '', 'wk', '', '', '']
    ]
    board = classic_board
    moves = []
    promotion_list = ['q', 'r', 'n', 'b']
    onscreen_promotion_list = ['bq', 'br', 'bn', 'bb']
    white_king_moved = False
    black_king_moved = False
    rooks_moved = [False, False, False, False]
    sizeOfPiece = ""
    pawn_promotion_position = []

    def __init__(self) -> None:
        pass

    def readjustPieces(self):
        for index, piece in enumerate(images):
            images[index][1] = pygame.transform.scale(piece[1], ((current_size[1]*0.7)/8.3, (current_size[1]*0.7)/8.3))
        self.sizeOfPiece = (current_size[1]*0.7)/8.3

    def drawBoard(self, screen):
        self.box_dimen = (current_size[1]*0.7) // 8
        self.board_x = current_size[0]*0.05
        self.board_y = 0.15*current_size[1]
        self.board_height = current_size[1]*0.7
        self.board_width = self.board_height
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(screen, BBLUE if ((i+1) % 2 == 0 and (j+1) % 2 != 0) or ((i+1) % 2 != 0 and (j+1)%2==0) else WHITE,
                            (current_size[0]*0.05+(i*self.box_dimen), 0.15*current_size[1]+(j*self.box_dimen), self.box_dimen, self.box_dimen))
        for y in range(0, 8):
            for x in range(0, 8):
                for piece in images:
                    if piece[0] == self.board[y][x]:
                        if y == piece_held[0] and x == piece_held[1]:
                            ...
                        else:
                            piece_rect = piece[1].get_rect()
                            piece_rect.center = (current_size[0]*0.05+(x*self.box_dimen)+(0.5*self.box_dimen), 0.15*current_size[1]+(y*self.box_dimen)+(0.5*self.box_dimen))
                            screen.blit(piece[1], piece_rect)

    def isValidMove(self, piece, piece_pos, end_pos, optional_enpassant=False):
        #Checking to make sure program doesnt accidentally count the user placing the piece back on the same square as a move
        if (piece_pos[0], piece_pos[1]) == (end_pos[0], end_pos[1]):
            return False
        if self.board[end_pos[0]][end_pos[1]] != "":
            if piece[0] == self.board[end_pos[0]][end_pos[1]][0]:
                return False
        if piece[1] == "p":
            if piece[0] == "w":
                if end_pos[1] == piece_pos[1]:
                    if abs(piece_pos[0] - end_pos[0]) == 2 and piece_pos[0] == 6:
                        if self.board[end_pos[0]][end_pos[1]] != "" or self.board[end_pos[0]+1][end_pos[1]] != "":
                            return False
                        return True
                    elif piece_pos[0] - end_pos[0] == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return False
                        return True
                elif end_pos[1] == piece_pos[1]+1 or end_pos[1] == piece_pos[1]-1:
                    if abs(piece_pos[0] - end_pos[0]) == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return True
                        if end_pos[0] == 2 and self.moves[-1][1] == "bp" and self.moves[-1][2][0] == 3 and (self.moves[-1][2][1] == piece_pos[1]+1 or self.moves[-1][2][1] == piece_pos[1]-1):
                            if optional_enpassant == True:
                                return None
                            return True
                    return False
                return False
            else:
                if end_pos[1] == piece_pos[1]:
                    if abs(piece_pos[0] - end_pos[0]) == 2 and piece_pos[0]==1:
                        if self.board[end_pos[0]][end_pos[1]] != "" or self.board[end_pos[0]-1][end_pos[1]] != "":
                            return False
                        return True
                    elif piece_pos[0] - end_pos[0] == -1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return False
                        return True
                elif end_pos[1] == piece_pos[1]+1 or end_pos[1] == piece_pos[1]-1:
                    if piece_pos[0] - end_pos[0] == -1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return True
                        if end_pos[0] == 5 and self.moves[-1][1] == "wp" and self.moves[-1][2][0] == 4 and (self.moves[-1][2][1] == piece_pos[1]+1 or self.moves[-1][2][1] == piece_pos[1]-1):
                            if optional_enpassant == True:
                                return None
                            return True
                    return False
                return False
        if piece[1] == "b":
            #Check for diagonal
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        if piece[1] == "n":
            if abs(end_pos[0]-piece_pos[0]) == 2 and abs(end_pos[1]-piece_pos[1]) == 1:
                return True
            elif  abs(end_pos[0]-piece_pos[0]) == 1 and abs(end_pos[1]-piece_pos[1]) == 2:
                return True
            return False
        if piece[1] == "r":
            if piece_pos[0] == end_pos[0] and piece_pos[1] != end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif piece_pos[0] != end_pos[0] and piece_pos[1] == end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        if piece[1] == "k":
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                if (abs(end_pos[0]-piece_pos[0]) == 1 and abs(end_pos[1]-piece_pos[1]) == 1):
                    return True
            elif (end_pos[0]==piece_pos[0]+1 or end_pos[0]==piece_pos[0]-1) and end_pos[1]==piece_pos[1]:
                return True 
            elif (end_pos[1]==piece_pos[1]+1 or end_pos[1]==piece_pos[1]-1) and end_pos[0]==piece_pos[0]:
                return True
            if piece[0] == "w":
                if self.white_king_moved == False:
                    if (end_pos[1] == 2 and self.rooks_moved[0] == False) or (end_pos[1] == 6 and self.rooks_moved[1] == False):
                        if self.isCheckWhileMoving(self.white_king, end_pos, 1 if end_pos[1] - piece_pos[1] > 0 else -1, "WHITE"):
                            return None
            else:
                if self.black_king_moved == False:
                    if (end_pos[1] == 2 and self.rooks_moved[2] == False) or (end_pos[1] == 6 and self.rooks_moved[3] == False):
                        if self.isCheckWhileMoving(self.black_king, end_pos, 1 if end_pos[1] - piece_pos[1] > 0 else -1, "BLACK"):
                            return None
            return False
        if piece[1] == "q":
            if piece_pos[0] == end_pos[0] and piece_pos[1] != end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif piece_pos[0] != end_pos[0] and piece_pos[1] == end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        return False
        
    def isCheckWhileMoving(self, start_pos, end_pos, direction, COLOUR):
        choice = "wk" if COLOUR == "WHITE" else "bk"
        for i in range(0, abs(end_pos[1]-start_pos[1])):
            if i > 0:
                if self.board[start_pos[0]][start_pos[1]+i*direction] != '':
                    return False
            if self.makeMove((start_pos[0], start_pos[1], choice), start_pos[0], start_pos[1]+(i*direction), True) == False:
                return False
        return True

    def isInCheck(self, optional_return_both=False):
        white_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and (abs(self.black_king[0]-index_x) == abs(self.black_king[1]-index_y) or (self.black_king[0]==index_x and self.black_king[1] != index_x) or (self.black_king[1]==index_y and self.black_king[0] != index_x) or (abs(self.black_king[0]-index_x) == 2 and abs(self.black_king[1]-index_y) == 1) or (abs(self.black_king[0]-index_x) == 1 and abs(self.black_king[1]-index_y) == 2))]
        black_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and (abs(self.white_king[0]-index_x) == abs(self.white_king[1]-index_y) or (self.white_king[0]==index_x and self.white_king[1] != index_x) or (self.white_king[1]==index_y and self.white_king[0] != index_x) or (abs(self.white_king[0]-index_x) == 2 and abs(self.white_king[1]-index_y) == 1) or (abs(self.white_king[0]-index_x) == 1 and abs(self.white_king[1]-index_y) == 2))]
        white_pieces_list = []
        black_check = False
        white_check = False
        for x in range(0, len(white_pieces)):
            if self.isValidMove(white_pieces[x][0], (white_pieces[x][1], white_pieces[x][2]), (self.black_king[0], self.black_king[1])) == True:
                white_pieces_list.append((white_pieces[x][1], white_pieces[x][2]))
        if len(white_pieces_list) > 0:
            if optional_return_both == False:
                return ("BLACK", white_pieces_list)
            black_check = True
        black_pieces_list = []
        for x in black_pieces:
            if self.isValidMove(x[0], (x[1], x[2]), (self.white_king[0], self.white_king[1])) == True:
                black_pieces_list.append((x[1], x[2]))
        if len(black_pieces_list) > 0:
            if optional_return_both == False:
                return ("WHITE", black_pieces_list)
            white_check = True
        if optional_return_both == False:
            return (False, "")
        if white_check and black_check:
            return (2, "")
        elif white_check:
            return ("WHITE", black_pieces_list)
        elif black_check:
            return ("BLACK", white_pieces_list)
        return (False, "")
    
    # canKingMove() can be used in both checking for CheckMates and StaleMates.

    def canKingMove(self, COLOUR):
        king = (deepcopy(self.white_king), 'wk') if COLOUR == "WHITE" else (deepcopy(self.black_king), 'bk')
        condition = False
        for row in range(-1, 2):
            for column in range(-1, 2):
                if (0 > row+king[0][0] or row+king[0][0] > 7 or 0 > column+king[0][1] or column+king[0][1] > 7) == False:
                    if self.isValidMove(king[1], king[0], [king[0][0]+row, king[0][1]+column]):
                            if COLOUR == "WHITE":
                                self.white_king = [king[0][0]+row, king[0][1]+column]
                            else:
                                self.black_king = [king[0][0]+row, king[0][1]+column]
                            tmp = self.board[king[0][0]+row][king[0][1]+column]
                            self.board[king[0][0]][king[0][1]] = ""
                            self.board[king[0][0]+row][king[0][1]+column]= king[1]
                            if self.isInCheck()[0] != COLOUR:
                                condition = True
                            if COLOUR == "WHITE":
                                self.white_king = [king[0][0]+row, king[0][1]+column]
                            else:
                                self.black_king = [king[0][0], king[0][1]]
                            self.board[king[0][0]][king[0][1]] = king[1]
                            self.board[king[0][0]+row][king[0][1]+column]= tmp
        if condition == True:
            return True
        return False

    def isCheckmate(self, COLOUR, checking_pieces):
        king = (deepcopy(self.white_king), 'wk') if COLOUR == "WHITE" else (deepcopy(self.black_king), 'bk')
        condition_1, condition_2, condition_3 = False, False, False

        # Condition 1 - Can the king escape check by moving to an adjacent square.
        condition_1 = self.canKingMove(COLOUR)
                            
        # Condition 2 - Can the checking piece be captured?
        if len(checking_pieces) == 1:
            if COLOUR == "WHITE":
                white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w"]
                for x in white_pieces:
                    #if self.isValidMove(x[0], [x[1], x[2]], [checking_pieces[0][0], checking_pieces[0][1]]):
                    if self.makeMove(x, checking_pieces[0][0], checking_pieces[0][1], True):
                        condition_2 = True   
                        
            elif COLOUR == "BLACK":
                black_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b"]
                for x in black_pieces:
                    if self.makeMove(x, checking_pieces[0][0], checking_pieces[0][1], True):
                        condition_2 = True

        # Condition 3 - Can the check be blocked by another piece
        if len(checking_pieces) == 1:
            positions = self.isValidDiagRow(king[0][0], king[0][1], checking_pieces[0][0], checking_pieces[0][1], optional_return_positions=True)
            black_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and y[1] != "k"]
            white_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and y[1] != "k"]
            if COLOUR == "WHITE":
                for x in white_pieces:
                    for j in positions:
                        if self.isValidMove(x[0], (x[1], x[2]), (j[0], j[1])):
                            condition_3 = True
            elif COLOUR == "BLACK":
                for x in black_pieces:
                    for j in positions:
                        if self.isValidMove(x[0], (x[1], x[2]), (j[0], j[1])):
                            condition_3 = True
        
        if condition_1 or condition_2 or condition_3:
            return False
        return True
        
    
    def isValidDiagRow(self, piece_row, piece_column, end_row, end_column, optional_return_positions=False):
        #Checking for the type of validation we will have to perform. rr/c stands for the step in the corresponding column/row
        rr = -1 if (piece_row - end_row) > 0 else 1
        rc = -1 if (piece_column - end_column) > 0 else 1
        iterAmount = piece_row-end_row
        optional_positions = []
        if end_column == piece_column:
            rc = 0
        elif end_row == piece_row:
            rr = 0
            iterAmount = piece_column-end_column
        for i in range(0, abs(iterAmount)-1):
            piece_row = piece_row + rr
            piece_column = piece_column + rc
            optional_positions.append((piece_row, piece_column))
            if self.board[piece_row][piece_column] != "":
                if optional_return_positions != True:
                    return False
        if optional_return_positions == True:
            return optional_positions
        return True
    
    def isStalemate(self):
        COLOUR = "WHITE" if board.move % 2 == 0 else "BLACK"
        if self.getAllMoves(COLOUR) == 0:
            print("IS STALEMATE")
            return True
        return False
    
    def getAllMoves(self, COLOUR):
        moves_list = []
        if COLOUR == "WHITE":
            white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w"]
            for piece in white_pieces:
                for row in range(0, 8):
                    for column in range(0, 8):
                        if self.makeMove(piece, row, column, optional_return=True) == True:
                            moves_list.append([piece, (row,column)])
            if len(moves_list) == 0:
                return 0
            return moves_list
                    
    #Optional return means no change is made 
    def makeMove(self, piece_held, row_clicked, column_clicked, optional_return=False, choice="", AI=False):
        boolean_validMove = self.isValidMove(piece_held[2], [piece_held[0], piece_held[1]], [row_clicked, column_clicked], optional_enpassant=True)
        if boolean_validMove == True:
            tmp = self.board[row_clicked][column_clicked]
            self.board[piece_held[0]][piece_held[1]] = ""
            self.board[row_clicked][column_clicked] = piece_held[2]
            if piece_held[2][1] == "k":
                if piece_held[2][0] == "w":
                    self.white_king =  [row_clicked, column_clicked]
                else:
                    self.black_king = [row_clicked, column_clicked]
            currentCheck = self.isInCheck(optional_return_both=True)[0]
            if ((currentCheck == "BLACK" and self.move % 2 != 0) or (currentCheck == "WHITE" and self.move % 2 == 0)) or currentCheck == 2:
                self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                self.board[row_clicked][column_clicked] = tmp
                if piece_held[2][1] == "k":
                    if piece_held[2][0] == "w":
                        self.white_king = [piece_held[0], piece_held[1]]
                    else:
                        self.black_king = [piece_held[0], piece_held[1]]
                if optional_return == True:
                    return False
            else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                if optional_return == True:
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    if piece_held[2][1] == "k":
                        if piece_held[2][0] == "w":
                            self.white_king = [piece_held[0], piece_held[1]]
                        else:
                            self.black_king = [piece_held[0], piece_held[1]]
                    return True
                if (piece_held[2] == "wp" and row_clicked == 0) or (piece_held[2] == "bp" and row_clicked == 7):
                    if AI == False:
                        global choice_making
                        choice_making = True
                        self.pawn_promotion_position = [row_clicked,column_clicked]
                    else:
                        self.board[row_clicked][column_clicked] = str(piece_held[2][0] + choice)
                    
                if piece_held[2] == "wk":
                    self.white_king = [row_clicked, column_clicked]
                    self.white_king_moved = True
                elif piece_held[2] == "bk":
                    self.black_king = [row_clicked, column_clicked]
                    self.black_king_moved = True
                elif piece_held[2] == "wr":
                    if piece_held[1] == 0:
                        self.rooks_moved[0] = True
                    else:
                        self.rooks_moved[1] = True
                elif piece_held[2] == "br":
                    if piece_held[1] == 0:
                        self.rooks_moved[2] = True
                    else:
                        self.rooks_moved[3] = True
                self.moves.append([board.move, piece_held[2], [row_clicked, column_clicked]])
                self.move = board.move + 1
            if optional_return == True:
                return False
        elif boolean_validMove == None:
            if piece_held[2][1] == "p":
                tmp = self.board[row_clicked][column_clicked]
                self.board[piece_held[0]][piece_held[1]] = ""
                self.board[row_clicked][column_clicked] = piece_held[2]
                tmp2 = self.board[row_clicked-(1 if piece_held[2][0] == "w" else -1)][column_clicked]
                self.board[row_clicked-(-1 if piece_held[2][0] == "w" else 1)][column_clicked] = ""
                if (self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0):
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    self.board[row_clicked-(1 if piece_held[2][0] == "w" else -1)][column_clicked] = tmp2
                    if optional_return == True:
                        return False
                else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                    if optional_return == True:
                        self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                        self.board[row_clicked][column_clicked] = tmp
                        return True
                    self.moves.append([board.move, piece_held[2], [row_clicked, column_clicked]])
                    self.move = board.move + 1
            elif piece_held[2][1] == "k":
                tmp = self.board[row_clicked][column_clicked]
                self.board[piece_held[0]][piece_held[1]] = ""
                self.board[row_clicked][column_clicked] = piece_held[2]
                if piece_held[2][1] == "k":
                    if piece_held[2][0] == "w":
                        self.white_king =  [row_clicked, column_clicked]
                    else:
                        self.black_king = [row_clicked, column_clicked]
                if (self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0):
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    if piece_held[2][1] == "k":
                        if piece_held[2][0] == "w":
                            self.white_king = [piece_held[0], piece_held[1]]
                        else:
                            self.black_king = [piece_held[0], piece_held[1]]
                    if optional_return == True:
                        return False
                else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                    if optional_return == True:
                        self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                        self.board[row_clicked][column_clicked] = tmp
                        if piece_held[2][1] == "k":
                            if piece_held[2][0] == "w":
                                self.white_king = [piece_held[0], piece_held[1]]
                            else:
                                self.black_king = [piece_held[0], piece_held[1]]
                        return True
                    if piece_held[2] == "wk":
                        self.white_king = [row_clicked, column_clicked]
                        if column_clicked == 2:
                            self.board[7][0] = ""
                            self.board[7][3] = "wr"
                        else:
                            self.board[7][7] = ""
                            self.board[7][5] = "wr"
                    elif piece_held[2] == "bk":
                        self.black_king = [row_clicked, column_clicked]
                        if column_clicked == 2:
                            self.board[0][0] = ""
                            self.board[0][3] = "br"
                        else:
                            self.board[0][7] = ""
                            self.board[0][5] = "br"
                    self.moves.append([board.move, piece_held[2], [row_clicked, column_clicked]])
                    self.move = board.move + 1

# Class for handling games between entitys/players, e.g time management.

class Game():
    player_one_time = 600
    player_two_time = 600
    startTime = 0
    lastTime = 0

    def __init__(self) -> None:
        pass

    def startGame(self):
        self.startTime = time.time()
    
    def updateTimer(self, player):
        if player == 1:
            self.player_one_time = self.player_one_time - 1
        else:
            self.player_two_time = self.player_two_time - 1
        self.lastTime = self.lastTime + 1
            
    # TODO: Return game result
    def __str__(self) -> str:
        return f"TODO"

newGame = Game()
newGame.startGame()

fullscreen = False

HOME_SCREEN = "HOME_SCREEN"
GAME_SCREEN = "GAME_SCREEN"

current_state = HOME_SCREEN


font_name = "freesansbold.ttf"
font_size = 32
font_color = (255, 255, 255)


font = pygame.font.Font(font_name, font_size)

# Section for declaring and rendering text

###
game_name = "CHESS"
text_surface = font.render(game_name, True, font_color)
game_name_rect = text_surface.get_rect()
game_name_rect.center = (current_size[0] // 2, current_size[1] // 10)
###
screen_player_one_timer = secondsToTime(newGame.player_one_time)
screen_player_one_timer_text_surface = font.render(screen_player_one_timer, True, WHITE)  # Render the text with black color
screen_player_one_timer_rect = screen_player_one_timer_text_surface.get_rect()
###
screen_player_two_timer = secondsToTime(newGame.player_two_time)
screen_player_two_timer_text_surface = font.render(screen_player_two_timer, True, WHITE)  # Render the text with black color
screen_player_two_timer_rect = screen_player_two_timer_text_surface.get_rect()

# Board related variables. NOTE: Should aim to integrate these in the board class

hold_click = False
piece_lock = False
piece_held = (9, 9, 'nn')

# Check to see if promotions box is made yet
flag_ismade = False
ai_thinking = False

board = Board()
board.readjustPieces()
pieces_rect = []
FPS = 30

def makeAIMove():
    depth = 4

    start_time = time.time()
    move = ai.startMiniMax(depth, board.board, board.move)
    print(f"Evaluation at depth {depth} with Transposition table took: {time.time()-start_time} seconds")
    print(f"Number of transpositions: {ai.transpositions}")
    print(f"Nodes per second (nps): {ai.nodes/(time.time()-start_time)}")
    board.makeMove(move[1][0], move[1][1][0], move[1][1][1], AI=True, choice="q")
    global FPS 
    FPS = 30
    global ai_thinking
    ai_thinking = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                done=True

            # Changing the screen size and ensuring elements change accordingly.
            if event.key == pygame.K_ESCAPE:
                
                if fullscreen:
                    current_size = (screen_width*0.5,  screen_height*0.5)
                    pygame.display.set_mode(current_size)
                    fullscreen = False
                    game_name_rect.center = (current_size[0] // 2, current_size[1] // 10)
                else:
                    current_size = ((screen_width, screen_height))
                    pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                    fullscreen = True
                    game_name_rect.center = (current_size[0] // 2, current_size[1] // 10)
                board.readjustPieces()
            # Resets the board to its original state. NOTE: Should soon aim to integrate into board class
            if event.key == pygame.K_r:
                #board.board = deepcopy(classic_board)
                board.move = 0
                board.black_king = [0, 4]
                board.white_king = [7, 4]
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    current_state = GAME_SCREEN
                mouse_pos = pygame.mouse.get_pos()
                if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:
                    hold_click = True
                if choice_making == True:
                    if flag_ismade == True:
                        mouse_pos = pygame.mouse.get_pos()
                        if box3.x < mouse_pos[0] < box3.x+box3.width and box3.y < mouse_pos[1] < box3.y+box3.height:
                            xpos_mouse = ((((mouse_pos[0]-box3.x-0.5*board.sizeOfPiece)/board.sizeOfPiece)-0.75) // 1)+1
                            pawn_pos = board.pawn_promotion_position
                            if pawn_pos[0] == 0:
                                board.board[pawn_pos[0]][pawn_pos[1]] = "w" + board.promotion_list[int(xpos_mouse)]
                            else:
                                board.board[pawn_pos[0]][pawn_pos[1]] = "b" + board.promotion_list[int(xpos_mouse)]
                            choice_making = False
                            flag_ismade = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if hold_click == True:
                if piece_lock == True:
                    if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:
                        if (piece_held[2][0] == "w" and board.move % 2 == 0) or (piece_held[2][0] == "b" and board.move % 2 != 0):
                            column_clicked = int((mouse_pos[0]-board.board_x) // board.box_dimen)
                            row_clicked = int((mouse_pos[1]-board.board_y) // board.box_dimen)
                            board.makeMove(piece_held, row_clicked, column_clicked)
                            """
                            if board.isValidMove(piece_held[2], [piece_held[0], piece_held[1]], [row_clicked, column_clicked]) == True:
                                board.board[piece_held[0]][piece_held[1]] = ""
                                board.board[row_clicked][column_clicked] = piece_held[2]
                                if piece_held[2] == "wk":
                                    board.white_king = [row_clicked, column_clicked]
                                elif piece_held[2] == "bk":
                                    board.black_king = [row_clicked, column_clicked]
                                board.move = board.move + 1
                            """
                hold_click = False
                piece_lock = False
                piece_held = (9, 9, 'nn')
    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:
        screen.blit(text_surface, game_name_rect)
    elif current_state == GAME_SCREEN:
        board.drawBoard(screen)

        ### DRAW THE BOARD
        box1 = pygame.draw.rect(screen, NEW, (board.board_x-current_size[0]*0.025, current_size[1]*0.025, (current_size[1]*0.7//8)*8+current_size[0]*0.05, current_size[1]*0.1))
        box2 = pygame.draw.rect(screen, NEW, (board.board_x-current_size[0]*0.025, current_size[1]*0.87, (current_size[1]*0.7)//8*8+current_size[0]*0.05, current_size[1]*0.1))
        if choice_making == True:
            box3 = pygame.draw.rect(screen, WHITE, [(board.board_x+0.5*board.board_width)-(2*board.sizeOfPiece)-(2.5*current_size[1]*0.01),
                                            board.board_y+0.5*board.board_height-(0.5*board.sizeOfPiece) -(2*current_size[1]*0.01), 4*board.sizeOfPiece+(5*current_size[1]*0.01), board.sizeOfPiece+2*current_size[1]*0.01])
            flag_ismade = True
            count = 0
            for piece in images:
                if piece[0] == board.onscreen_promotion_list[count]:
                    piece_rect = piece[1].get_rect()
                    piece_rect.center = [box3.x+(count+0.75)*board.sizeOfPiece, 
                                        box3.y+0.5*box3.height]
                    screen.blit(piece[1], piece_rect)
                    count = count + 1
                if count == 4:
                    break
        #Timer
        if int(time.time() - newGame.startTime) > newGame.lastTime:
            #board.getAllMoves("WHITE")
            """
            #print(board.isInCheck())
            if (board.isInCheck())[0] == "BLACK":
                if board.isCheckmate("BLACK", board.isInCheck()[1]):
                    print("White wins!")
            if board.isInCheck()[0] == "WHITE":
                if board.isCheckmate("WHITE", board.isInCheck()[1]):
                    print("Black wins!")
                    """
            newGame.updateTimer((1 if board.move % 2 == 0 else 2))
            
            screen_player_one_timer = secondsToTime(newGame.player_one_time)
            screen_player_one_timer_text_surface = font.render(screen_player_one_timer, True, WHITE)
            screen_player_one_timer_rect = screen_player_one_timer_text_surface.get_rect()
            screen_player_one_timer_rect.center = box2.center
            ###
            screen_player_two_timer = secondsToTime(newGame.player_two_time)
            screen_player_two_timer_text_surface = font.render(screen_player_two_timer, True, WHITE)
            screen_player_two_timer_rect = screen_player_two_timer_text_surface.get_rect()
            screen_player_two_timer_rect.center = box1.center
        
        
        screen.blit(screen_player_one_timer_text_surface, screen_player_one_timer_rect)
        screen.blit(screen_player_two_timer_text_surface, screen_player_two_timer_rect)
        if board.move % 2 == 0 and ai_thinking == False:
            ai_thinking = True
            FPS = 1
            move = ""
            t1 = threading.Thread(target=makeAIMove, args=())
            t1.start()
        if hold_click == True:
            mouse_pos = pygame.mouse.get_pos()
            column_clicked = int((mouse_pos[0]-board.board_x) // board.box_dimen)
            row_clicked = int((mouse_pos[1]-board.board_y) // board.box_dimen)
            if (board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height) == False and hold_click == True:
                    hold_click = False
                    piece_lock = False
                    continue
            if piece_lock == True:
                type_piece = pygame.transform.scale(type_piece, ((current_size[1]*0.7)/7.0, (current_size[1]*0.7)/7.0))
                piece_rect = type_piece.get_rect()
                piece_rect.center = (mouse_pos[0], mouse_pos[1])
                screen.blit(type_piece, piece_rect)
            else:
                try:
                    if board.board[row_clicked][column_clicked] != "":
                        for piece in images:
                            if piece[0] == board.board[row_clicked][column_clicked]:
                                new_piece = pygame.transform.scale(piece[1], ((current_size[1]*0.7)/7.0, (current_size[1]*0.7)/7.0))
                                piece_rect = new_piece.get_rect()
                                piece_rect.center = (mouse_pos[0], mouse_pos[1])
                                screen.blit(new_piece, piece_rect)
                                piece_held = (row_clicked, column_clicked, piece[0])
                                piece_lock = True
                                type_piece = piece[1]
                except Exception as e:
                    ...
    pygame.display.flip()
    clock.tick(FPS)

t1.join()
pygame.quit()