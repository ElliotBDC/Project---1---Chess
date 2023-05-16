import pygame


class addButtonListener():
    events = []
    def __init__(self) -> None:
        pass

    def addButton(self, id, x, y, width, height, text, font_colour, font_size, font="freesansbold.ttf"):
        self.events.append([id, x, y, width, height])
        font = pygame.font.Font(font, font_size)
        text_surface = font.render(text, True, font_colour)

        

