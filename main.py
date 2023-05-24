import pygame
import pygame_plus

#Colours (pygame requires them to be in binary representation)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
#For the chess board
GREEN = (118,150,86)
 
pygame.init()
 
#Declaring the screen size
screen_size = pygame.display.Info()
screen_width = screen_size.current_w
screen_height = screen_size.current_h
current_size = (screen_width*0.5,  screen_height*0.5)
screen = pygame.display.set_mode(current_size)
done = False

clock = pygame.time.Clock()
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

"""
wp = ['wp', pygame.image.load("images/wp.png")]
wr = ['wr', pygame.image.load("images/wr.png")]
wb = ['wb', pygame.image.load("images/wb.png")]
wn = ['wn', pygame.image.load("images/wn.png")]
wq = ['wq', pygame.image.load("images/wq.png")]
wk = ['wk', pygame.image.load("images/wk.png")]
bp = ['bp', pygame.image.load("images/bp.png")]
bq = ['bq', pygame.image.load("images/bq.png")]
br = ['br', pygame.image.load("images/br.png")]
bn = ['bn', pygame.image.load("images/bn.png")]
bb = ['bb', pygame.image.load("images/bb.png")]
bk = ['bk', pygame.image.load("images/bk.png")]
"""


class Board():
    board_x = current_size[0]*0.05
    board_y = 0.15*current_size[1]
    board_height = current_size[1]*0.7
    board_width = board_height
    box_dimen = (current_size[1]*0.7) // 8
    move = 0
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
    #262626

    def drawBoard(self, screen):
        self.box_dimen = (current_size[1]*0.7) // 8
        self.board_x = current_size[0]*0.05
        self.board_y = 0.15*current_size[1]
        self.board_height = current_size[1]*0.7
        self.board_width = self.board_height
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(screen, GREEN if ((i+1) % 2 == 0 and (j+1) % 2 != 0) or ((i+1) % 2 != 0 and (j+1)%2==0) else WHITE,
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
        ### TODO
        if piece[1] == "p":
            print("1")
            if piece[0] == "w":
                print("2")
                print(end_pos, piece_pos)
                if end_pos[0] == piece_pos[0]:
                    print("3")
                    if end_pos[1] - piece_pos[1] == 1:
                        print("4")
                        return True
            else:
                if end_pos[0] == piece_pos[0]:
                    if end_pos[1] - piece_pos[1] == 1:
                        return True
        if piece[1] == "b":
            ...
        if piece[1] == "n":
            ...
        if piece[1] == "r":
            ...
        if piece[1] == "k":
            ...


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

BACKGROUND_COLOUR_1 = hex_to_rgb('#262626')

fullscreen = False

HOME_SCREEN = "HOME_SCREEN"
GAME_SCREEN = "GAME_SCREEN"

current_state = HOME_SCREEN

text = "Chess"
font_name = "freesansbold.ttf"
font_size = 32
font_color = (255, 255, 255)

font = pygame.font.Font(font_name, font_size)
text_surface = font.render(text, True, font_color)

text_rect = text_surface.get_rect()
text_rect.center = (current_size[0] // 2, current_size[1] // 10)

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
            if event.key == pygame.K_ESCAPE:
                ### The following code is used to make sure the size of features on the page are changed according to the current
                ### size of the program
                if fullscreen:
                    current_size = (screen_width*0.5,  screen_height*0.5)
                    pygame.display.set_mode(current_size)
                    fullscreen = False

                    text_rect.center = (current_size[0] // 2, current_size[1] // 10)
                else:
                    current_size = ((screen_width, screen_height))
                    pygame.display.set_mode(current_size, pygame.FULLSCREEN)
                    fullscreen = True

                    text_rect.center = (current_size[0] // 2, current_size[1] // 10)
                ###
                ###
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
                                board.board[piece_held[0]][piece_held[1]] = ""
                                board.board[row_clicked][column_clicked] = piece_held[2]
                                board.move = board.move + 1
                hold_click = False
                piece_lock = False
                piece_held = (9, 9, 'nn')

    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:
        
        screen.blit(text_surface, text_rect)
    elif current_state == GAME_SCREEN:
        board.drawBoard(screen)
        ### DRAW THE BOARD
        pygame.draw.rect(screen, BLACK, (board.board_x-current_size[0]*0.025, current_size[1]*0.025, (current_size[1]*0.7//8)*8+current_size[0]*0.05, current_size[1]*0.1))
        pygame.draw.rect(screen, BLACK, (board.board_x-current_size[0]*0.025, current_size[1]*0.87, (current_size[1]*0.7)//8*8+current_size[0]*0.05, current_size[1]*0.1))
        if hold_click == True:
            mouse_pos = pygame.mouse.get_pos()
            column_clicked = int((mouse_pos[0]-board.board_x) // board.box_dimen)
            row_clicked = int((mouse_pos[1]-board.board_y) // board.box_dimen)
            if (board.board_x+board.board_width > mouse_pos[0] > board.board_x and board.board_y < mouse_pos[1] < board.board_y+board.board_height) == False and hold_click == True:
                    hold_click = False
                    piece_lock = False
                    continue
            print(row_clicked, column_clicked)
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
                    

            print(row_clicked, column_clicked)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

