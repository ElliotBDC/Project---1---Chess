import pygame

#Colours (pygame requires them to be in binary representation)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
#For the chess board
GREEN = (118,150,86)
 
pygame.init()
 
#Declaring the screen size
size = (3720, 1920)
screen = pygame.display.set_mode(size)
done = False

clock = pygame.time.Clock()
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    screen.fill(WHITE)
    pygame.display.flip()


    #Screen refreshes at 60 times per second. 60 FPS
    clock.tick(60)
pygame.quit()

