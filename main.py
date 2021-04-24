# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021


import sys
import random
import pygame
from pygame.locals import *

win_width = 600
win_height = 400
done = False
pygame.init()
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Gradient Rect")

colour_list = [[(0,0,255), (0,255,0), (255,0,255), (255,255,0)],[(255,0,255), (0,255,0), (0,0,255), (255,255,0)],[(0,255,255), (0,255,0), (255,0,255), (255,255,0)]]
sprite_list = pygame.sprite.Group()

def fill_rect_window():
    pygame.draw.rect(window, (0, 0, 0), (0, 0, 200, 400))

def rect_window_padding():
    pygame.draw.rect(window, (0, 0, 0), (0,0, 200, 20))
    pygame.draw.rect(window, (0, 0, 0), (0,380, 200, 20))


class Rect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 40])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.colour = colour

def sprites (colour_list, sprite_list):
    for i in range(0, 3):
        for j in range (0, 4):
            sprite_list.add(Rect(20+(40*j), (20*(i+1)) + (40*i), colour_list[i][j]))
    return sprite_list

sprites(colour_list, sprite_list)

sprite_list.draw(window)

pygame.display.update()

# This is the main entry point to the game.
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEWHEEL:
            if event.y == -1:
                for sprite in sprite_list:
                    sprite.rect.y -= 20
                    print (sprite.rect.y)
                fill_rect_window()
                sprite_list.draw(window)
                rect_window_padding()
            pygame.display.flip()
            if event.y == 1:
                for sprite in sprite_list:
                    sprite.rect.y += 20
                    print (sprite.rect.y)
                fill_rect_window()
                sprite_list.draw(window)
                rect_window_padding()
            pygame.display.flip()

pygame.quit()

# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")