# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import random
import pygame

DEBUG = False

# todo: BIG BRAINED THINGS SO I DONT FORGET
# for the circles can u have like semi transparent things? like can u adjust opacity if u can u could totally
# create two classes (or one class) and have a like self.transparent and if ur on hover
# and then create two sprite lists one for the base colour and one for like a black overlay
# and then do a like for loop ot see if hovering on top of a circle and if on top of a circle
# and then if on top of a circle change the like overlay_sprite_list sprite to self.transparent = false 

class Rect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, colour, win_vars, id):
        pygame.sprite.Sprite.__init__(self)

        # todo: this surface needs to scale wrt window size. (checkmark)
        self.image = pygame.Surface([win_vars["sprite_size"], win_vars["sprite_size"]])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.colour = colour
        self.clicked = False
        self.id = id


class Circle(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([400, 400])  # todo: variables tomorrow pls
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.id = id


def addCircleSprites(sprite_list2, colour_list, win_vars):
    for i in range(0, win_vars["num_of_rectangles"]):
        sprite_list2.add(Circle(colour_list[i], 200, 0, i))  # todo: variables tomorrow pls
    return sprite_list2  # todo: pls rename these things


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


def updateSprites(sprite_list, window, win_height, win_vars):
    pygame.draw.rect(window, win_vars["black"], (0, 0, win_vars["width_sidebar"], win_height))
    sprite_list.draw(window)
    pygame.draw.rect(window, win_vars["black"], (0, 0, win_vars["width_sidebar"], win_vars["bar_thickness"]))
    pygame.draw.rect(window, win_vars["black"],
                     (0, win_vars["bottom_bar_loc"], win_vars["width_sidebar"], win_vars["bar_thickness"]))


def addSidebarSprites(sprite_list, colour_list, win_vars):
    for i in range(0, win_vars["num_of_rectangles"]):
        for j in range(0, 4):
            sprite_list.add(
                Rect(win_vars["bar_thickness"] + (win_vars["sprite_size"] * j),
                     (win_vars["bar_thickness"] * (i + 1)) + (win_vars["sprite_size"] * i), colour_list[i][j],
                     win_vars, i))
    return sprite_list


# This is the main entry point to the game.

def sidebar():
    # todo: anni will create a proper init function to set these variables.
    # init
    win_size = 600, 400
    done = False
    pygame.init()
    window = pygame.display.set_mode((win_size[0], win_size[1]))
    pygame.display.set_caption("Gradient Rect")

    # todo: multiple colours loaded from levels file?
    colour_list = [[(0, 0, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)],
                   [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
                   [(0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0)]]
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    sprite_list = pygame.sprite.Group()
    sprite_list2 = pygame.sprite.Group()
    single_sprite_list = pygame.sprite.GroupSingle()

    # calculating variables
    win_vars = {
        "bar_thickness": win_size[1] * 0.05,
        "sprite_size": ((win_size[0] / 3) - (win_size[1] * 0.1)) / 4,
        "width_sidebar": win_size[0] / 3,
        "bottom_bar_loc": win_size[1] * 0.95,
        "black": (0, 0, 0),
        "num_of_rectangles": 3
    }

    # -----------------------------
    # Chris you can probably get away with grouping win_width, win_height, sidebar_width, bar_thickness into one tuple.
    # I'll probably also make a configurator for the settings that will return all of these as a list or tuple.
    # -----------------------------

    # displaying sprites
    sprite_list = addSidebarSprites(sprite_list, colour_list, win_vars)
    sprite_list2 = addCircleSprites(sprite_list2, colour_list_circle, win_vars)
    sprite_list.draw(window)
    pygame.display.update()

    # running the game
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEWHEEL:
                if pygame.mouse.get_pos()[0] < win_vars["width_sidebar"]:
                    if event.y == -1:
                        for rect_sprite in sprite_list:
                            rect_sprite.rect.y -= win_vars["bar_thickness"]
                            if DEBUG: print(rect_sprite.rect.y)
                        updateSprites(sprite_list, window, win_size[1], win_vars)
                        pygame.display.flip()
                    else:
                        for rect_sprite in sprite_list:
                            rect_sprite.rect.y += win_vars["bar_thickness"]
                            if DEBUG: print(rect_sprite.rect.y)
                        updateSprites(sprite_list, window, win_size[1], win_vars)
                        pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect_sprite in sprite_list:
                    if rect_sprite.rect.collidepoint(pos):
                        rect_sprite.clicked = True

            for rect_sprite in sprite_list:
                if rect_sprite.clicked == True:
                    temp_id = rect_sprite.id
                    for circle_sprite in sprite_list2:
                        if circle_sprite.id == temp_id:
                            single_sprite_list.add(circle_sprite)
                    rect_sprite.clicked = False
            single_sprite_list.draw(window)
            pygame.display.flip()

    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")
    sidebar()
    print("bleppers")
