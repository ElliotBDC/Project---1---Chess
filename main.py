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
 


class Board():
    board_x = None
    board_y = None
    board_width = None 
    board_height = None
    board = [
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '']
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    current_state = GAME_SCREEN

    screen.fill(BACKGROUND_COLOUR_1)
    if current_state == HOME_SCREEN:
        
        screen.blit(text_surface, text_rect)
    elif current_state == GAME_SCREEN:
        board.drawBoard(screen)
        pygame.draw.rect(screen, BLACK, (board.board_x-int(current_size[0]*0.01), int(current_size[1]*0.025), int(((current_size[1]*0.7)//8)*8+current_size[0]*0.05)), int(current_size[1]*0.1))
        pygame.draw.rect(screen, BLACK, (board.board_x-int(current_size[0]*0.025), current_size[1]*0.875, int(((current_size[1]*0.7)//8)*8+current_size[0]*0.05)), current_size[1]*0.1)
 



    pygame.display.flip()
    clock.tick(60)
pygame.quit()

