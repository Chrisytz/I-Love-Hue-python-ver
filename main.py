# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import random
import pygame
from pygame.locals import *


class Rect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, colour, dictionary):
        pygame.sprite.Sprite.__init__(self)

        # todo: this surface needs to scale wrt window size. (checkmark)
        self.image = pygame.Surface([dictionary["sprite_size"], dictionary["sprite_size"]])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.colour = colour


# class Display():
#     def __init__(self, win_width, win_height):
#         self.win_width = win_width
#         self.win_height = win_height
#         self.bar_thickness = win_height * 0.05
#         self.sprite_size = ((win_width / 3) - (win_height * 0.1)) / 4
#         self.width_sidebar = win_width / 3
#         self.bottom_bar_loc = win_height * 0.95
#         self.done = False
#         pygame.init()
#         self.window = pygame.display.set_mode((win_width, win_height))
#         pygame.display.set_caption("Gradient Rect")


def updateSprites(sprite_list, window, win_height, dictionary):
    black = (0, 0, 0)
    pygame.draw.rect(window, black, (0, 0, dictionary["width_sidebar"], win_height))
    sprite_list.draw(window)
    pygame.draw.rect(window, black, (0, 0, dictionary["width_sidebar"], dictionary["bar_thickness"]))
    pygame.draw.rect(window, black,
                     (0, dictionary["bottom_bar_loc"], dictionary["width_sidebar"], dictionary["bar_thickness"]))


def addSidebarSprites(sprite_list, colour_list, dictionary):
    for i in range(0, 3):
        for j in range(0, 4):
            sprite_list.add(
                Rect(dictionary["bar_thickness"] + (dictionary["sprite_size"] * j),
                     (dictionary["bar_thickness"] * (i + 1)) + (dictionary["sprite_size"] * i), colour_list[i][j],
                     dictionary))
    return sprite_list


# This is the main entry point to the game.

def sidebar():
    # todo: anni will create a proper init function to set these variables.
    # init
    win_size = [600, 400]
    done = False
    pygame.init()
    window = pygame.display.set_mode((win_size[0], win_size[1]))
    pygame.display.set_caption("Gradient Rect")

    # todo: multiple colours loaded from levels file?
    colour_list = [[(0, 0, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)],
                   [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
                   [(0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)]]
    sprite_list = pygame.sprite.Group()

    # calculating variables
    dictionary = {
        "bar_thickness": win_size[1] * 0.05,
        "sprite_size": ((win_size[0] / 3) - (win_size[1] * 0.1)) / 4,
        "width_sidebar": win_size[0] / 3,
        "bottom_bar_loc": win_size[1] * 0.95
    }

    # -----------------------------
    # Chris you can probably get away with grouping win_width, win_height, sidebar_width, bar_thickness into one tuple.
    # I'll probably also make a configurator for the settings that will return all of these as a list or tuple.
    # -----------------------------

    # displaying sprites
    sprite_list = addSidebarSprites(sprite_list, colour_list, dictionary)
    sprite_list.draw(window)
    pygame.display.update()

    # running the game
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == MOUSEWHEEL:
                if pygame.mouse.get_pos()[0] < dictionary["width_sidebar"]:
                    if event.y == -1:
                        for sprite in sprite_list:
                            sprite.rect.y -= dictionary["bar_thickness"]
                            print(sprite.rect.y)
                        updateSprites(sprite_list, window, win_size[1], dictionary)
                        pygame.display.flip()
                    else:
                        for sprite in sprite_list:
                            sprite.rect.y += dictionary["bar_thickness"]
                            print(sprite.rect.y)
                        updateSprites(sprite_list, window, win_size[1], dictionary)
                        pygame.display.flip()
    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")
    sidebar()
