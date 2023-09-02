import pygame
import time
import board
import database

# Declaring colours in binary format

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (118,150,86)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

BACKGROUND_COLOUR_1 = (6, 4, 2)
BACKGROUND_COLOUR_1 = hex_to_rgb('#262626')
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
WP = 'colour + piece'
e.g WP = 'white' (W) + 'pawn' (P) hence -> WP
"""

WP = pygame.image.load("images/wP.svg")
WR = pygame.image.load("images/wR.svg")
WB = pygame.image.load("images/wB.svg")
WN = pygame.image.load("images/wN.svg")
WQ = pygame.image.load("images/wQ.svg")
WK = pygame.image.load("images/wK.svg")
BP = pygame.image.load("images/bP.svg")
BQ = pygame.image.load("images/bQ.svg")
BR = pygame.image.load("images/bR.svg")
BN = pygame.image.load("images/bN.svg")
BB = pygame.image.load("images/bB.svg")
BK = pygame.image.load("images/bK.svg")
pygame.display.set_icon(BP)

images = [
    ['WP', WP],
    ['WR', WR],
    ['WB', WB],
    ['WN', WN],
    ['WQ', WQ],
    ['WK', WK],
    ['BP', BP],
    ['BQ', BQ],
    ['BR', BR],
    ['BN', BN],
    ['BB', BB],
    ['BK', BK]
]
classic_board = [
    ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
    ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
    ['', ' ', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
    ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
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

# Variable used when paWN is promoted and player needs to choose replacing piece

choice_making = False

# Declaring the class for the chess board (functionality & design)

newBoard = board.Board()

class Board():
    # Display Properties
    board_x = current_size[0]*0.05
    board_y = 0.15*current_size[1]
    board_height = current_size[1]*0.7
    board_width = board_height
    box_dimen = (current_size[1]*0.7) // 8

    #Board 
    move = 0
    board = newBoard.mailboard
    moves = []
    promotion_list = ['Q', 'R', 'N', 'B']
    onscreen_promotion_list = ['BQ', 'BR', 'BN', 'BB']

    def __init__(self) -> None:
        pass

    def readjustPieces(self):
        for index, piece in enumerate(images):
            images[index][1] = pygame.transform.scale(piece[1], ((current_size[1]*0.7)/8.3, (current_size[1]*0.7)/8.3))
        self.sizeOfPiece = (current_size[1]*0.7)/8.3

    def draWBoard(self, screen):
        self.board = newBoard.mailboard
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
LOGIN_SCREEN = "LOGIN_SCREEN"
THANKS_SCREEN = "THANKS_SCREEN"

current_state = LOGIN_SCREEN


font_name = "freesansbold.ttf"
font_size = 25
font_color = (255, 255, 255)


font = pygame.font.Font(font_name, font_size)
title_font = pygame.font.Font(font_name, 30)
smaller_font = pygame.font.Font(font_name, 20)

# Section for declaring and rendering text

SQUARE_WIDTH = int(current_size[0] / 6) 
CENTER = current_size[0] // 2
WIDTH = current_size[0] * 0.4
HEIGHT = current_size[1] * 0.13

###
text_1 = "Play vs AI"
text_1_surface = smaller_font.render(text_1, True, WHITE)
text_1_rect = text_1_surface.get_rect()
text_1_rect.center = (SQUARE_WIDTH * 3.5, SQUARE_WIDTH * 1.5)
###
#text_2 = "Play online"
#text_2_surface = font.render(text_2, True, WHITE)
#text_2_rect = text_2_surface.get_rect()
#text_2_rect.center = (SQUARE_WIDTH * 4, SQUARE_WIDTH * 2)
###
text_3 = "2 Player"
text_3_surface = smaller_font.render(text_3, True, WHITE)
text_3_rect = text_3_surface.get_rect()
text_3_rect.center = (SQUARE_WIDTH * 4.5, SQUARE_WIDTH * 2.5)
###

text_5 = "Chess AI Trainer"
text_5_surface = title_font.render(text_5, True, WHITE)
text_5_rect = text_5_surface.get_rect()
text_5_rect.center = (current_size[0]//2, current_size[1]//7)
###
text_6 = "New? Register here"
text_6_surface = smaller_font.render(text_6, True, WHITE)
text_6_rect = text_6_surface.get_rect()
text_6_rect.center = (CENTER, current_size[1]*0.6+HEIGHT*2)
###
text_7 = "Username: "
text_7_surface = font.render(text_7, True, WHITE)
text_7_rect = text_7_surface.get_rect()
text_7_rect.center = (CENTER - text_7_rect.width, current_size[1]*0.35)
###
text_8 = "Password: "
text_8_surface = font.render(text_8, True, WHITE)
text_8_rect = text_8_surface.get_rect()
text_8_rect.center = (CENTER - text_7_rect.width, current_size[1]*0.55)
###
text_11 = "Thanks for registering. Click anywhere to continue."
text_11_surface = title_font.render(text_11, True, WHITE)
text_11_rect = text_11_surface.get_rect()
text_11_rect.center = (current_size[0]//2, current_size[1]//7)

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
hovering = False
hover_1 = False
hover_2 = False
registering = False

# Variables to check whether an username or password is being entered. (To check for key presses)
username_entry = False
password_entry = False

username_contents = ""
password_contents = ""

option_1_rect = pygame.Rect(SQUARE_WIDTH*3, SQUARE_WIDTH*1, SQUARE_WIDTH, SQUARE_WIDTH)
option_2_rect = pygame.Rect(SQUARE_WIDTH*4, SQUARE_WIDTH*2, SQUARE_WIDTH, SQUARE_WIDTH)
username_3_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.41, current_size[0]//3.6, current_size[1]*0.08)
password_4_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.61, current_size[0]//3.6, current_size[1]*0.08)

###
username_9_text = ""
text_9_surface = font.render(username_9_text, True, WHITE)
text_9_rect = text_9_surface.get_rect()
text_9_rect.centerx = text_7_rect.left + 10
text_9_rect.centery = username_3_rect.centery
###
password_10_text = ""
text_10_surface = font.render(password_10_text, True, WHITE)
text_10_rect = text_10_surface.get_rect()
text_10_rect.centerx = text_7_rect.left + 10
text_10_rect.centery = password_4_rect.centery

board = Board()
board.readjustPieces()
pieces_rect = []
FPS = 30

while not done:
    for event in pygame.event.get():
        if current_state == HOME_SCREEN:
            if option_1_rect.collidepoint(pygame.mouse.get_pos()):
                hovering = True
                hover_1 = True
                hover_2 = False
            elif option_2_rect.collidepoint(pygame.mouse.get_pos()):
                hovering = True
                hover_2 = True
                hover_1 = False
            else:
                hovering = False
                hover_2 = False
                hover_1 = False
            
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            ### Dealing with login key entrys
            print(f"{ord('a')} + {ord('z')} + {ord('A')} + {ord('Z')} + {ord('0')} + {ord('9')} ")
            if current_state == LOGIN_SCREEN:
                if username_entry == True:
                    if len(username_contents) <= 11:
                        if 57 >= event.key >= 48 or 90 >= event.key >= 65 or 122 >= event.key >= 97: 
                            username_contents += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            username_contents = username_contents[0:len(username_contents)-1]
                        elif event.key == pygame.K_RETURN:
                            username_entry = False
                        username_9_text = username_contents
                        text_9_surface = font.render(username_9_text, True, WHITE)
                if password_entry == True:
                    if 57 >= event.key >= 48 or 90 >= event.key >= 65 or 122 >= event.key >= 97: 
                        password_contents += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        password_contents = password_contents[0:len(password_contents)-1]
                    elif event.key == pygame.K_RETURN:
                        if registering == True:
                            if database.registerUser(username_contents, password_contents):
                                current_state = THANKS_SCREEN
                            else:
                                text_5 = f"The name {username_contents} is already in use"
                                text_5_surface = title_font.render(text_5, True, RED)
                                text_5_rect = text_5_surface.get_rect()
                                text_5_rect.center = (current_size[0]//2, current_size[1]//7)
                        else:
                            if database.checkUserData(username_contents, password_contents):
                                current_state = HOME_SCREEN
                            else:
                                password_entry = False
                    password_10_text = '*' * len(password_contents)
                    text_10_surface = font.render(password_10_text, True, WHITE)


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
                    text_1_rect.center = (SQUARE_WIDTH * 3.5, SQUARE_WIDTH * 1.5)
                    text_3_rect.center = (SQUARE_WIDTH * 4.5, SQUARE_WIDTH * 2.5)

                    option_1_rect = pygame.Rect(SQUARE_WIDTH*3, SQUARE_WIDTH*1, SQUARE_WIDTH, SQUARE_WIDTH)
                    option_2_rect = pygame.Rect(SQUARE_WIDTH*4, SQUARE_WIDTH*2, SQUARE_WIDTH, SQUARE_WIDTH)

                    username_3_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.41, current_size[0]//3.6, current_size[1]*0.08)
                    password_4_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.61, current_size[0]//3.6, current_size[1]*0.08)

                else:
                    current_size = ((screen_width, screen_height))
                    pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                    fullscreen = True
                    SQUARE_WIDTH = int(current_size[0] / 8) 
                    font_size = 40
                    font = pygame.font.Font(font_name, font_size)
                    text_surface = font.render(text_1, True, WHITE)
                    text_1_rect.center = (SQUARE_WIDTH * 3.5, SQUARE_WIDTH * 1.5)
                    text_3_rect.center = (SQUARE_WIDTH * 4.5, SQUARE_WIDTH * 2.5)

                    option_1_rect = pygame.Rect(SQUARE_WIDTH*3, SQUARE_WIDTH*1, SQUARE_WIDTH, SQUARE_WIDTH)
                    option_2_rect = pygame.Rect(SQUARE_WIDTH*4, SQUARE_WIDTH*2, SQUARE_WIDTH, SQUARE_WIDTH)

                    username_3_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.41, current_size[0]//3.6, current_size[1]*0.08)
                    password_4_rect = pygame.Rect(CENTER - 1.5*text_7_rect.width, current_size[1]*0.61, current_size[0]//3.6, current_size[1]*0.08)
                    

                board.readjustPieces()
            # Resets the board to its original state. NOTE: Should soon aim to integrate into board class
            if event.key == pygame.K_r:
                board.move = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
                #if event.button == 1:
                    #current_state = GAME_SCREEN
                if current_state == GAME_SCREEN:
                    mouse_pos = pygame.mouse.get_pos()
                    if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:
                        hold_click = True
                    if choice_making == True:
                        if flag_ismade == True:
                            mouse_pos = pygame.mouse.get_pos()
                            if box3.x < mouse_pos[0] < box3.x+box3.width and box3.y < mouse_pos[1] < box3.y+box3.height:
                                possible_moves = newBoard.getAllMoves()
                                xpos_mouse = ((((mouse_pos[0]-box3.x-0.5*board.sizeOfPiece)/board.sizeOfPiece)-0.75) // 1)+1
                                for i in range(0, len(possible_moves)-5, 5):
                                    if possible_moves[i:i+4][2] == board.promotion_list[int(xpos_mouse)].upper():
                                        newBoard.makeMove(possible_moves[i:i+5])
                                        board.move+=1
                                        break
                                choice_making = False
                                flag_ismade = False
                elif current_state == LOGIN_SCREEN:
                    if username_3_rect.collidepoint(pygame.mouse.get_pos()):
                        username_entry = True
                        password_entry = False
                    elif password_4_rect.collidepoint(pygame.mouse.get_pos()):
                        password_entry = True
                        username_entry = False
                    elif text_6_rect.collidepoint(pygame.mouse.get_pos()):
                        if registering == False:
                            registering = True
                            text_5 = "Please enter your details below"
                            text_5_surface = title_font.render(text_5, True, WHITE)
                            text_5_rect = text_5_surface.get_rect()
                            text_5_rect.center = (current_size[0]//2, current_size[1]//7)
                            text_6 = "Already have an account?"
                            text_6_surface = smaller_font.render(text_6, True, WHITE)
                            text_6_rect = text_6_surface.get_rect()
                            text_6_rect.center = (CENTER, current_size[1]*0.6+HEIGHT*2)
                        else:
                            text_6 = "New? Register here"
                            text_6_surface = smaller_font.render(text_6, True, WHITE)
                            text_6_rect = text_6_surface.get_rect()
                            text_6_rect.center = (CENTER, current_size[1]*0.6+HEIGHT*2)
                            text_5 = "Chess AI Trainer"
                            text_5_surface = title_font.render(text_5, True, WHITE)
                            text_5_rect = text_5_surface.get_rect()
                            text_5_rect.center = (current_size[0]//2, current_size[1]//7)
                            registering = False
                    else:
                        username_entry = False
                        password_entry = False


        elif event.type == pygame.MOUSEBUTTONUP:
            if hold_click == True:
                if piece_lock == True:
                    if board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height:

                        if (piece_held[2][0] == "W" and newBoard.WhitePlayerMove == True) or (piece_held[2][0] == "B" and newBoard.WhitePlayerMove == False):
                            column_clicked = int((mouse_pos[0]-board.board_x) // board.box_dimen)
                            row_clicked = int((mouse_pos[1]-board.board_y) // board.box_dimen)
                            move = str(7-piece_held[0])+str(7-piece_held[1]) + str(7-row_clicked)+str(7-column_clicked)
                            possible_moves = newBoard.getAllMoves()
                            print(f"Move: {move} + Poss: {possible_moves}")

                            for i in range(0, len(possible_moves), 5):
                                if (type(move[2]) == int) == True: 
                                    print(newBoard.moveToAlgebra(possible_moves[i:i+4])+possible_moves[i+4:i+5])

                            if (piece_held[2] == "WP" and 7-row_clicked == 7) or (piece_held[2] == "BP" and 7-row_clicked == 0):
                                choice_making = True
                                
                            for i in range(0, len(possible_moves)):
                                if move == possible_moves[i:i+4]:
                                    newBoard.makeMove(possible_moves[i:i+5])
                                    board.move+=1
                            
                hold_click = False
                piece_lock = False
                piece_held = (9, 9, 'nn')
            if current_state == HOME_SCREEN:
                if option_1_rect.collidepoint(pygame.mouse.get_pos()) or option_2_rect.collidepoint(pygame.mouse.get_pos()):
                    current_state = GAME_SCREEN
    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == LOGIN_SCREEN:
        screen.blit(text_5_surface, text_5_rect)
        screen.blit(text_7_surface, text_7_rect)
        screen.blit(text_8_surface, text_8_rect)
        screen.blit(text_6_surface, text_6_rect)
        screen.blit(text_9_surface, text_9_rect)
        screen.blit(text_10_surface, text_10_rect)

        # Username box
        username_box = pygame.draw.rect(screen, WHITE, [CENTER - 1.5*text_7_rect.width, current_size[1]*0.41, current_size[0]//3.6, current_size[1]*0.08], 3)

        # Password box
        password_box = pygame.draw.rect(screen, WHITE, [CENTER - 1.5*text_7_rect.width, current_size[1]*0.61, current_size[0]//3.6, current_size[1]*0.08], 3)

    elif current_state == THANKS_SCREEN:
        screen.blit(text_11_surface, text_11_rect)
































    elif current_state == HOME_SCREEN:
        if hovering == True:
            screen.fill((0, 0, 0))

        ### Background Decoration
        count = 0
        for y in range(0, int(current_size[1]), SQUARE_WIDTH):
                for x in range(0, int(current_size[0]//4), SQUARE_WIDTH):
                    if count % 2 == 0:
                        colour = BACKGROUND_COLOUR_2
                    else:
                        colour = BACKGROUND_COLOUR_3
                    if hovering == True:
                        if hover_2 == True:
                            print(f"{SQUARE_WIDTH} + {x}")
                            if y == (SQUARE_WIDTH * 2):
                                print("HELLO")
                                pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=20)

                    else:
                        pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH))
                    count+=1
        count = 0
        for y in range(0, int(current_size[1]), SQUARE_WIDTH):
                for x in range(int(current_size[0]), int(current_size[0]//(4)), -SQUARE_WIDTH):
                    if count % 2 == 0:
                        colour = BACKGROUND_COLOUR_2
                    else:
                        colour = BACKGROUND_COLOUR_3
                    if hovering == True:
                        if hover_1 == True:
                            print(f"{SQUARE_WIDTH} + {x}")
                            if fullscreen:
                                if x == int(current_size[0]) - SQUARE_WIDTH * 5:
                                    pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=20)
                            else:
                                if x == int(current_size[0]) - SQUARE_WIDTH * 3:
                                    pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=20)
                        if hover_2 == True:
                            if y == SQUARE_WIDTH * 2:
                                pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=20)

                    else:
                        pygame.draw.rect(screen, colour, (x, y, SQUARE_WIDTH, SQUARE_WIDTH), border_radius=20)
                    count+=1

        #if hovering == True:
        #    if hover_1 == True:
        #        pygame.draw.rect(screen, BLACK, [SQUARE_WIDTH*3, SQUARE_WIDTH*1, SQUARE_WIDTH, SQUARE_WIDTH])
        #    if hover_2 == True:
        #        pygame.draw.rect(screen, BLACK, [SQUARE_WIDTH*4, SQUARE_WIDTH*2, SQUARE_WIDTH, SQUARE_WIDTH])
        if hovering == True:
            if hover_1 == True:
                screen.blit(text_1_surface, text_1_rect)
            else:
                screen.blit(text_3_surface, text_3_rect)
        else:
            screen.blit(text_1_surface, text_1_rect)
            #screen.blit(text_2_surface, text_2_rect)
            screen.blit(text_3_surface, text_3_rect)
        
        

    elif current_state == GAME_SCREEN:
        board.draWBoard(screen)
        
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

pygame.quit()