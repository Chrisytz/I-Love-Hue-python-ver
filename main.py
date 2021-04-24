# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import random
import pygame
from pygame.locals import *


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


def updateSprites(sprite_list, window, win_height, width_sidebar, bar_thickness, bottom_bar_loc):
    pygame.draw.rect(window, (0, 0, 0), (0, 0, width_sidebar, win_height))
    sprite_list.draw(window)
    pygame.draw.rect(window, (0, 0, 0), (0, 0, width_sidebar, bar_thickness))
    pygame.draw.rect(window, (0, 0, 0), (0, bottom_bar_loc, width_sidebar, bar_thickness))


def addSidebarSprites(sprite_list, colour_list, bar_thickness, rect_size):
    for i in range(0, 3):
        for j in range(0, 4):
            sprite_list.add(
                Rect(bar_thickness + (rect_size * j), (bar_thickness * (i + 1)) + (rect_size * i), colour_list[i][j]))
    return sprite_list


# This is the main entry point to the game.

def sidebar():
    # init
    win_width = 600
    win_height = 400
    done = False
    pygame.init()
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Gradient Rect")

    colour_list = [[(0, 0, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)],
                   [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
                   [(0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)]]
    sprite_list = pygame.sprite.Group()

    # calculating variables
    bar_thickness = win_height * 0.05
    rect_size = ((win_width / 3) - (win_height * 0.1)) / 4
    width_sidebar = win_width / 3
    bottom_bar_loc = win_height * 0.95

    # displaying sprites
    sprite_list = addSidebarSprites(sprite_list, colour_list, bar_thickness, rect_size)
    sprite_list.draw(window)
    pygame.display.update()

    # running the game
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == MOUSEWHEEL:
                if pygame.mouse.get_pos()[0] < win_width / 3:
                    if event.y == -1:
                        for sprite in sprite_list:
                            sprite.rect.y -= 20
                            print(sprite.rect.y)
                        updateSprites(sprite_list, window, win_height, width_sidebar, bar_thickness, bottom_bar_loc)
                        pygame.display.flip()
                    else:
                        for sprite in sprite_list:
                            sprite.rect.y += 20
                            print(sprite.rect.y)
                        updateSprites(sprite_list, window, win_height, width_sidebar, bar_thickness, bottom_bar_loc)
                        pygame.display.flip()
    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")
    sidebar()
