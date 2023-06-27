import pygame
import time
from copy import deepcopy

# Declaring colours in binary format

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (118,150,86)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

BACKGROUND_COLOUR_1 = hex_to_rgb('#262626')
BACKGROUND_COLOUR_1 = hex_to_rgb('#272932')
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

# Declaring the class for the chess board (functionality & design)

class Board():
    board_x = current_size[0]*0.05
    board_y = 0.15*current_size[1]
    board_height = current_size[1]*0.7
    board_width = board_height
    box_dimen = (current_size[1]*0.7) // 8
    move = 0
    white_king = [7, 4]
    black_king = [0, 4]
    board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]

    def __init__(self) -> None:
        pass

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
                            new_piece = pygame.transform.scale(piece[1], ((current_size[1]*0.7)/8.3, (current_size[1]*0.7)/8.3))
                            piece_rect = new_piece.get_rect()
                            piece_rect.center = (current_size[0]*0.05+(x*self.box_dimen)+(0.5*self.box_dimen), 0.15*current_size[1]+(y*self.box_dimen)+(0.5*self.box_dimen))
                            screen.blit(new_piece, piece_rect)

    def isValidMove(self, piece, piece_pos, end_pos):
        #Checking to make sure program doesnt accidentally count the user placing the piece back on the same square as a move
        if (piece_pos[0], piece_pos[1]) == (end_pos[0], end_pos[1]):
            return False
        if self.board[end_pos[0]][end_pos[1]] != "":
            if piece[0] == self.board[end_pos[0]][end_pos[1]][0]:
                return False
        ###TODO moves into check
        if self.isInCheck()[0] != False:
            return False
        if piece[1] == "p":
            if piece[0] == "w":
                if end_pos[1] == piece_pos[1]:
                    if piece_pos[0] - end_pos[0] == 2 and piece_pos[0] == 6:
                        if self.board[end_pos[0]][end_pos[1]] != "" or self.board[end_pos[0]+1][end_pos[1]] != "":
                            return False
                        return True
                    elif piece_pos[0] - end_pos[0] == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return False
                        return True
                elif end_pos[1] == piece_pos[1]+1 or end_pos[1] == piece_pos[1]-1:
                    if piece_pos[0] - end_pos[0] == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return True
                        
                    return False
            else:
                if end_pos[1] == piece_pos[1]:
                    if piece_pos[0] - end_pos[0] == -2 and piece_pos[0]==1:
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
                    return False
        if piece[1] == "b":
            #Check for diagonal
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
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
        if piece[1] == "k":
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                if (abs(end_pos[0]-piece_pos[0]) == 1 and abs(end_pos[1]-piece_pos[1]) == 1):
                    return True
            elif (end_pos[0]==piece_pos[0]+1 or end_pos[0]==piece_pos[0]-1) and end_pos[1]==piece_pos[1]:
                return True 
            elif (end_pos[1]==piece_pos[1]+1 or end_pos[1]==piece_pos[1]-1) and end_pos[0]==piece_pos[0]:
                return True
            return False
        if piece[1] == "q":
            if piece_pos[0] == end_pos[0] and piece_pos[1] != end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif piece_pos[0] != end_pos[0] and piece_pos[1] == end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False


    def isInCheck(self):
        white_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and (abs(self.black_king[0]-index_x) == abs(self.black_king[1]-index_y) or (self.black_king[0]==index_x and self.black_king[1] != index_x) or (self.black_king[1]==index_y and self.black_king[0] != index_x) or (abs(self.black_king[0]-index_x) == 2 and abs(self.black_king[1]-index_y) == 1) or (abs(self.black_king[0]-index_x) == 1 and abs(self.black_king[1]-index_y) == 2))]
        black_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and (abs(self.white_king[0]-index_x) == abs(self.white_king[1]-index_y) or (self.white_king[0]==index_x and self.white_king[1] != index_x) or (self.white_king[1]==index_y and self.white_king[0] != index_x) or (abs(self.white_king[0]-index_x) == 2 and abs(self.white_king[1]-index_y) == 1) or (abs(self.white_king[0]-index_x) == 1 and abs(self.white_king[1]-index_y) == 2))]
        white_pieces_list = []
        for x in range(0, len(white_pieces)):
            if self.isValidMove(white_pieces[x][0], (white_pieces[x][1], white_pieces[x][2]), (self.black_king[0], self.black_king[1])) == True:
                white_pieces_list.append((white_pieces[x][1], white_pieces[x][2]))
        if len(white_pieces_list) > 0:
            print("BLACK CHECK & WHITE PIECES LIST: " + str(white_pieces_list))
            return ("BLACK", white_pieces_list)
        black_pieces_list = []
        for x in black_pieces:
            if self.isValidMove(x[0], (x[1], x[2]), (self.white_king[0], self.white_king[1])) == True:
                black_pieces_list.append((x[1], x[2]))
        if len(black_pieces_list) > 0:
            print("WHITE CHECK & LIST OF BLACK PIECES: " + str(black_pieces_list))
            return ("WHITE", black_pieces_list)
        return (False, "")
    
    def isCheckmate(self, COLOUR, checking_pieces):
        king = (deepcopy(self.white_king), 'wk') if COLOUR == "WHITE" else (deepcopy(self.black_king), 'bk')
        condition_1, condition_2, condition_3 = False, False, False

        # Condition 1 - Can the king escape check by moving to an adjacent square.
        for row in range(-1, 2):
            for column in range(-1, 2):
                if (0 > row+king[0][0] or row+king[0][0] > 7 or 0 > column+king[0][1] or column+king[0][1] > 7) == False:
                    if king[1] == "bk":
                            if self.isValidMove('bk', king[0], [king[0][0]+row, king[0][1]+column]):
                                    self.black_king = [king[0][0]+row, king[0][1]+column]
                                    if self.isInCheck()[0] == "BLACK":
                                        ...
                                    else: 
                                        print("Square to escape to: " + str((king[0][0]+row, king[0][1]+column)))
                                        self.black_king = [king[0][0], king[0][1]]
                                        condition_1 = True
                    else:
                            if self.isValidMove('wk', king[0], [king[0][0]+row, king[0][1]+column]):
                                    self.white_king = [king[0][0]+row, king[0][1]+column]
                                    if self.isInCheck()[0] == "WHITE":
                                        ...
                                    else: 
                                        print("Square to escape to: " + str((king[0][0]+row, king[0][1]+column)))
                                        self.white_king = [king[0][0], king[0][1]]
                                        condition_1 = True
                
                            
        # Condition 2 - Can the checking piece be captured?
        if len(checking_pieces) == 1:
            if COLOUR == "WHITE":
                black_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and y != "bk"]
                for x in black_pieces:
                    if self.isValidMove(x[0], (x[1], x[2]), (checking_pieces[0][0], checking_pieces[0][1])):
                        condition_2 = True
            elif COLOUR == "BLACK":
                white_pieces = [(y, index_x, index_y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and y != "wk"]
                for x in white_pieces:
                    if self.isValidMove(x[0], (x[1], x[2]), (checking_pieces[0][0], checking_pieces[0][1])):
                        condition_2 = True
            else:
                raise Exception
        else:
            ...

        # Condition 3 - Can the check be blocked by another piece
        if len(checking_pieces) == 1:
            #print(checking_pieces)
            positions = self.isValidDiagRow(king[0][0], king[0][1], checking_pieces[0][0], checking_pieces[0][1], optional_return_positions=True)
            #print(king)
            #print(positions)
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
                            print("Blocking piece: " + str(x))
                            condition_3 = True
            else:
                raise Exception

        else:
            ...
        
        self.black_king = [king[0][0], king[0][1]]
        if condition_1 or condition_2 or condition_3:
            print("Can the king escape via an adjacent square: " + str(condition_1))
            print("Can he checking piece be captured: " + str(condition_2))
            print("Can the check be blocked by another piece: " + str(condition_3))
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
            optional_positions.append((piece_row, piece_column))
            piece_row = piece_row + rr
            piece_column = piece_column + rc
            if self.board[piece_row][piece_column] != "":
                if optional_return_positions != True:
                    return False
        if optional_return_positions == True:
            return optional_positions
        return True

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

board = Board()

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
            
            # Resets the board to its original state. NOTE: Should soon aim to integrate into board class
            if event.key == pygame.K_r:
                board.board = deepcopy(classic_board)
                board.move = 0
                board.black_king = [0, 4]
                board.white_king = [7, 4]
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    current_state = GAME_SCREEN
                mouse_pos = pygame.mouse.get_pos()
                if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:
                    hold_click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if hold_click == True:
                if piece_lock == True:
                    if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:
                        if (piece_held[2][0] == "w" and board.move % 2 == 0) or (piece_held[2][0] == "b" and board.move % 2 != 0):
                            column_clicked = int((mouse_pos[0]-board.board_x) // board.box_dimen)
                            row_clicked = int((mouse_pos[1]-board.board_y) // board.box_dimen)
                            if board.isValidMove(piece_held[2], [piece_held[0], piece_held[1]], [row_clicked, column_clicked]) == True:
                                if piece_held[2] == "wk":
                                    board.white_king = [row_clicked, column_clicked]
                                elif piece_held[2] == "bk":
                                    board.black_king = [row_clicked, column_clicked]
                                board.board[piece_held[0]][piece_held[1]] = ""
                                board.board[row_clicked][column_clicked] = piece_held[2]
                                board.move = board.move + 1
                hold_click = False
                piece_lock = False
                piece_held = (9, 9, 'nn')

    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:
        screen.blit(text_surface, game_name_rect)
    elif current_state == GAME_SCREEN:
        #print(board.isInCheck())
        
        board.drawBoard(screen)
        ### DRAW THE BOARD
        box1 = pygame.draw.rect(screen, NEW, (board.board_x-current_size[0]*0.025, current_size[1]*0.025, (current_size[1]*0.7//8)*8+current_size[0]*0.05, current_size[1]*0.1))
        box2 = pygame.draw.rect(screen, NEW, (board.board_x-current_size[0]*0.025, current_size[1]*0.87, (current_size[1]*0.7)//8*8+current_size[0]*0.05, current_size[1]*0.1))
    
        #Timer
        if int(time.time() - newGame.startTime) > newGame.lastTime:
            print(board.isInCheck())
            if (board.isInCheck())[0] == "BLACK":
                if board.isCheckmate("BLACK", board.isInCheck()[1]):
                    print("CHECKMATE!!")
                else:
                    print("BLACK KING IS IN CHECK")
            if board.isInCheck()[0] == "WHITE":
                if board.isCheckmate("WHITE", board.isInCheck()[1]):
                    print("WHITE IS IN CHECKMATE!!")
                else:
                    print("WHITE IS IN CHECK")
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
    clock.tick(30)
pygame.quit()