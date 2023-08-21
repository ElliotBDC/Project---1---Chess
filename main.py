import pygame
import time
from copy import deepcopy
import server
# Declaring colours in binary format

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (118,150,86)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

BACKGROUND_COLOUR_1 = (6, 4, 2)#hex_to_rgb('#262626')
#BACKGROUND_COLOUR_1 = hex_to_rgb('#272932')
BBLUE = hex_to_rgb('#BA8C63')
NEW = hex_to_rgb('#114b5f')
BACKGROUND_COLOUR_2 = hex_to_rgb('#815438')
BACKGROUND_COLOUR_3 = hex_to_rgb('#F3DDBC')

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

wp = pygame.image.load("images/wP.svg")
wr = pygame.image.load("images/wR.svg")
wb = pygame.image.load("images/wB.svg")
wn = pygame.image.load("images/wN.svg")
wq = pygame.image.load("images/wQ.svg")
wk = pygame.image.load("images/wK.svg")
bp = pygame.image.load("images/bP.svg")
bq = pygame.image.load("images/bQ.svg")
br = pygame.image.load("images/bR.svg")
bn = pygame.image.load("images/bN.svg")
bb = pygame.image.load("images/bB.svg")
bk = pygame.image.load("images/bK.svg")
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
    ['', ' ', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]

def moveToAlgebra(move):
        moveString = chr(ord(move[1])+49) + str(8-int(move[0])) + chr(ord(move[3])+49) + str(8-int(move[2]))
        return moveString

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
    moves_this_turn = ""

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
title_font = pygame.font.Font(font_name, 30)
smaller_font = pygame.font.Font(font_name, 15)

# Section for declaring and rendering text

SQUARE_WIDTH = int(current_size[0] / 6) 
CENTER = current_size[0] // 2
WIDTH = current_size[0] * 0.4
HEIGHT = current_size[1] * 0.13

###
text_1 = "Play vs AI"
text_1_surface = font.render(text_1, True, WHITE)
text_1_rect = text_1_surface.get_rect()
text_1_rect.center = (SQUARE_WIDTH * 1.5, SQUARE_WIDTH * 1)
###
text_2 = "Play online"
text_2_surface = font.render(text_2, True, WHITE)
text_2_rect = text_2_surface.get_rect()
text_2_rect.center = (SQUARE_WIDTH * 1.5, SQUARE_WIDTH * 2)
###
text_3 = "Play offline"
text_3_surface = font.render(text_3, True, WHITE)
text_3_rect = text_3_surface.get_rect()
text_3_rect.center = (SQUARE_WIDTH * 1.5, SQUARE_WIDTH * 3)
###

text_5 = "Welcome to Chess"
text_5_surface = title_font.render(text_5, True, WHITE)
text_5_rect = text_5_surface.get_rect()
text_5_rect.center = (current_size[0]//2, current_size[1]//7)
###
text_6 = "New? Register here"
text_6_surface = smaller_font.render(text_6, True, BLACK)
text_6_rect = text_6_surface.get_rect()
text_6_rect.center = (CENTER, current_size[1]*0.6+HEIGHT*2)
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
waiting_tbc_verified = [2, ""]

# Check to see if promotions box is made yet
flag_ismade = False
ai_thinking = False

board = Board()
board.readjustPieces()
pieces_rect = []
FPS = 30

import threading

#t1 = threading.Thread(target=server.startServer, args=())
#t1.start()

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
                    SQUARE_WIDTH = int(current_size[0] / 6) 
                    font_size = 20
                    font = pygame.font.Font(font_name, font_size)
                    text_surface = font.render(text_1, True, WHITE)
                    text_1_rect.center = (SQUARE_WIDTH * 1.5, SQUARE_WIDTH * 1.5)
                else:
                    current_size = ((screen_width, screen_height))
                    pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                    fullscreen = True
                    SQUARE_WIDTH = int(current_size[0] / 6) 
                    font_size = 40
                    font = pygame.font.Font(font_name, font_size)
                    text_surface = font.render(text_1, True, WHITE)
                    text_1_rect.center = (SQUARE_WIDTH * 1.5, SQUARE_WIDTH * 1.5)
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
                            move = str(piece_held[0])+str(piece_held[1]) + str(row_clicked)+str(column_clicked)
                            print(f"{move}")
                            server.sendMessage(move)
                            waiting_tbc_verified = [board.board[piece_held[0]][piece_held[1]], move]
                            board.board[piece_held[0]][piece_held[1]] = ""
                            #board.makeMove(piece_held, row_clicked, column_clicked)
                hold_click = False
                piece_lock = False
                piece_held = (9, 9, 'nn')
    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:

        """
        ### Background Decoration
        SQUARE_WIDTH = int(current_size[0] / 6) 
        count = 0
        for y in range(0, int(current_size[1]), SQUARE_WIDTH):
            for x in range(0, int(current_size[0]), SQUARE_WIDTH):
                if count % 2 == 0:
                    colour = BACKGROUND_COLOUR_2
                else:
                    colour = BACKGROUND_COLOUR_3
                pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=40)
                count+=1
        """
        screen.blit(text_1_surface, text_1_rect)
        screen.blit(text_2_surface, text_2_rect)
        screen.blit(text_3_surface, text_3_rect)
        
        

    elif current_state == GAME_SCREEN:
        board.drawBoard(screen)
        """
        if waiting_tbc_verified[-1] != "":
            if server.verified[-1] == waiting_tbc_verified[-1]:
                x1, y1 = int(waiting_tbc_verified[-1][0]),int(waiting_tbc_verified[-1][1]) 
                x2, y2 = int(waiting_tbc_verified[-1][2]),int(waiting_tbc_verified[-1][3])
                #tmp = deepcopy(board.board[x2][y2])
                board.board[x2][y2] = waiting_tbc_verified[0]#board.board[x1][y1]
                board.board[x1][y1] = ""
                waiting_tbc_verified = [1, ""]
        """
        ### DRAW THE BOARD
        top1x= board.board_x-current_size[0]*0.025
        top1y = current_size[1]*0.025
        bottom1x, bottom2y = board.board_x-current_size[0]*0.025, current_size[1]*0.87
        width = (current_size[1]*0.7//8)*8+current_size[0]*0.05
        height = current_size[1]*0.1
       # print(f"{top1x} + {top1y} + {width} + {height}")
        box1 = pygame.draw.rect(screen, BACKGROUND_COLOUR_1, (top1x, top1y, (current_size[1]*0.7//8)*8+current_size[0]*0.05, current_size[1]*0.1))
        box2 = pygame.draw.rect(screen, BACKGROUND_COLOUR_1, (board.board_x-current_size[0]*0.025, current_size[1]*0.87, (current_size[1]*0.7)//8*8+current_size[0]*0.05, current_size[1]*0.1))
        line1 = pygame.draw.line(screen, WHITE, (top1x, top1y+height), (top1x+width, top1y+height), 2)
        line2 = pygame.draw.line(screen, WHITE, (bottom1x, bottom2y), (bottom1x+width, bottom2y), 2)
        
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
            #print(f"Waitingtbc {waiting_tbc_verified}")
            #print(f"Server.ver {server.verified}")
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
    clock.tick(FPS)

#t1.join()
pygame.quit()