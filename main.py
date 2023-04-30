import pygame

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
    board = {
        "a1": "R", "b1": "N", "c1": "B", "d1": "Q", "e1": "K", "f1": "B", "g1": "N", "h1": "R",
        "a2": "P", "b2": "P", "c2": "P", "d2": "P", "e2": "P", "f2": "P", "g2": "-", "h2": "P", 
        "a3": "-", "b3": "-", "c3": "-", "d3": "-", "e3": "-", "f3": "-", "g3": "-", "h3": "-",
        "a4": "-", "b4": "-", "c4": "-", "d4": "-", "e4": "-", "f4": "-", "g4": "-", "h4": "-",
        "a5": "-", "b5": "-", "c5": "-", "d5": "-", "e5": "-", "f5": "-", "g5": "-", "h5": "-",
        "a6": "-", "b6": "-", "c6": "-", "d6": "-", "e6": "-", "f6": "-", "g6": "-", "h6": "-",
        "a7": "P", "b7": "P", "c7": "P", "d7": "P", "e7": "P", "f7": "P", "g7": "P", "h7": "P",
        "a8": "-", "b8": "-", "c8": "-", "d8": "-", "e8": "-", "f8": "-", "g8": "-", "h8": "-",
    }
    def __init__(self) -> None:
        pass
    #262626

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
 



    pygame.display.flip()
    clock.tick(60)
pygame.quit()

