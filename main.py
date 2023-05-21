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
    board_x = None
    board_y = None
    board_width = None 
    board_height = None
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
        box_dimen = (current_size[1]*0.7) // 8
        self.board_x = current_size[0]*0.05
        self.board_y = 0.15*current_size[1]
        self.board_height = current_size[1]*0.7
        self.board_width = self.board_height
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(screen, GREEN if ((i+1) % 2 == 0 and (j+1) % 2 != 0) or ((i+1) % 2 != 0 and (j+1)%2==0) else WHITE,
                                (current_size[0]*0.05+(i*box_dimen), 0.15*current_size[1]+(j*box_dimen), box_dimen, box_dimen))
        for y in range(0, 8):
            for x in range(0, 8):
                for piece in images:
                    if piece[0] == self.board[y][x]:
                        new_piece = pygame.transform.scale(piece[1], ((current_size[1]*0.7)/8.3, (current_size[1]*0.7)/8.3))
                        piece_rect = new_piece.get_rect()
                        piece_rect.center = (current_size[0]*0.05+(x*box_dimen)+(0.5*box_dimen), 0.15*current_size[1]+(y*box_dimen)+(0.5*box_dimen))
                        screen.blit(new_piece, piece_rect)



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

    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:
        
        screen.blit(text_surface, text_rect)
    elif current_state == GAME_SCREEN:
        board.drawBoard(screen)
        ### DRAW THE BOARD
        pygame.draw.rect(screen, BLACK, (board.board_x-current_size[0]*0.025, current_size[1]*0.025, (current_size[1]*0.7//8)*8+current_size[0]*0.05, current_size[1]*0.1))
        pygame.draw.rect(screen, BLACK, (board.board_x-current_size[0]*0.025, current_size[1]*0.87, (current_size[1]*0.7)//8*8+current_size[0]*0.05, current_size[1]*0.1))
        


    pygame.display.flip()
    clock.tick(30)
pygame.quit()

