# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import random
import pygame
from level import runGame

DEBUG = False


# todo: BIG BRAINED THINGS SO I DONT FORGET
# diff num of squares (4x4, 8x8, 10x10)
# find some way to show the difficulty of each level
# one the side of each lvl --> #moves, home, restart --> smth smth import the shuffle function or wtv


class Rect(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, colour, win_vars, level_id):
        pygame.sprite.Sprite.__init__(self)

        # todo: this surface needs to scale wrt window size. (checkmark)
        self.image = pygame.Surface([win_vars["sprite_size"], win_vars["sprite_size"]])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        # self.colour = colour
        self.level_id = level_id  ## what the fuck is level id chris?!?


class Circle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, win_vars, circle_list, i, j, pos_id, list_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(circle_list[list_id][j]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.pos_id = pos_id  # pos id corresponds to the position of the thing on a level
        self.i = i
        self.j = j
        self.list_id = list_id  ## list id corresponds to the fucking LIST you put it ni you boNOBO
        # list ID currently corresponds to the STAGE or SET of colours.
        self.complete = False


class OverlayNumbers(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, number_list, number_list_blk, i, j, id, list_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(number_list[id]).convert_alpha()
        self.img_blk = pygame.image.load(number_list_blk[id]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.id = id
        self.i = i
        self.j = j
        self.list_id = list_id
        self.complete = False
        # print("printing id",id)

    def update_image(self, complete):
        self.complete = True
        self.image = self.img_blk
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def fillImage(self):
        self.image.set_alpha(0)


class Overlay(pygame.sprite.Sprite):
    # overlay is a really bad name but that's ok we will go with it
    def __init__(self, colour, x_pos, y_pos, win_vars, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((win_vars["circle_size"], win_vars["circle_size"]))
        self._original_colour = colour
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.hover = False
        self.clicked = False
        self.id = id
        self.complete = False

    def getOriginalColour(self):
        return self._original_colour

    def fillImage(self, alpha):
        self.image.set_alpha(alpha)
        self.image.fill(self.colour)


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

# # Utils
# todo: chris will fill
#  def rectangleEventHandler(event, pos):
#      if event.type == pygame.MOUSEWHEEL:
#          if pygame.mouse.get_pos()[0] < win_vars["width_sidebar"]:
#              if event.y == -1:
#                  for rect_sprite in sprite_list:
#                      rect_sprite.rect.y -= win_vars["bar_thickness"]
#                      if DEBUG: print(rect_sprite.rect.y)
#                  updateSprites(sprite_list, window, win_size[1], win_vars)
#                  pygame.display.flip()
#              else:
#                  for rect_sprite in sprite_list:
#                      rect_sprite.rect.y += win_vars["bar_thickness"]
#                      if DEBUG: print(rect_sprite.rect.y)
#                  updateSprites(sprite_list, window, win_size[1], win_vars)
#                  pygame.display.flip()

# if event.type == pygame.MOUSEBUTTONDOWN:
#     if event.button == 1:
#         pos = pygame.mouse.get_pos()
#         for rect_sprite in sprite_list:
#             if rect_sprite.rect.collidepoint(pos):
#                 rect_sprite.clicked = True

def updateSprites(sprite_list, window, win_height, win_vars):
    """ updates the sidebar sprites in a really crude manner."""
    pass
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


def addCircleSprites(background_colour, colour_list_circle, number_list_white, number_list_black, circle_sprites,
                     overlay_sprites, number_sprites, win_vars, level_id):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            circle_sprites.add(Circle((win_vars["width_sidebar"] + win_vars["bar_thickness"]) + j * (
                    win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars["bar_thickness"] + i * (
                                              win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars, colour_list_circle, i, count, count, level_id)) #OKAY SO I CHANGED THE FIRST COUNT FROM J TO COUNT it should work
            overlay_sprites.add(Overlay(background_colour,
                                        (win_vars["width_sidebar"] + win_vars["bar_thickness"]) + j * (
                                                win_vars["circle_size"] + win_vars["space_between_circles"]),
                                        win_vars["bar_thickness"] + i * (
                                                win_vars["circle_size"] + win_vars["space_between_circles"]), win_vars,
                                        count))
            number_sprites.add(OverlayNumbers((win_vars["width_sidebar"] + win_vars["bar_thickness"]) + j * (
                    win_vars["circle_size"] + win_vars["space_between_circles"]),
                                              win_vars["bar_thickness"] + i * (
                                                      win_vars["circle_size"] + win_vars["space_between_circles"]),
                                              number_list_white, number_list_black, i, j, count, level_id))
            count += 1

    return circle_sprites


# def addNumberSprites(win_vars, number_list_white, number_list_black, number_sprites, id):
#     count = 0
#     for i in range(0, 3):
#         for j in range(0, 3):
#             number_sprites.add(OverlayNumbers((win_vars["width_sidebar"] + win_vars["bar_thickness"]) + j * (
#                     win_vars["circle_size"] + win_vars["space_between_circles"]),
#                                               win_vars["bar_thickness"] + i * (
#                                                       win_vars["circle_size"] + win_vars["space_between_circles"]),
#                                               number_list_white, number_list_black, i, j, count, level_id))
#             count += 1
#     return number_sprites


# no longer drawing ellipses on top of sprites, its just drawing the sprites --> id is which rectangle was clicked so what colours to draw
def drawCircles(window, circle_sprites, id):
    # print(id)
    circle_sprites[id].draw(window)


def draw(window, number_sprites):
    for sprite in number_sprites:
        window.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


def loadCircles(circle_list, win_vars):
    loaded_circle_list = []
    count = 0
    for circle in circle_list:
        loaded_circle_list.append(pygame.image.load(circle_list[0][count]))
        count += 1
    return loaded_circle_list


def addColours(colour_list, rect_clicked, circle_clicked):
    colour = []
    for i in range(0, 4):
        colour.append(colour_list[rect_clicked][circle_clicked][i])
    return colour


def generateLists(list_of_circle_sprites, list_of_overlay_sprites, list_of_number_sprites, number):
    for i in range(0, number):
        list_of_circle_sprites[number] = pygame.sprite.Group()
        list_of_overlay_sprites[number] = pygame.sprite.Group()
        list_of_number_sprites[number] = pygame.sprite.Group()


# This is the main entry point to the game.

def sidebar():
    # todo: anni will create a proper init function to set these variables.
    # init
    win_size = 600, 400
    done = False
    background_colour = (255, 255, 255)
    pygame.init()
    window = pygame.display.set_mode((win_size[0], win_size[1]))
    pygame.display.set_caption("Gradient Rect")

    # calculating variables
    win_vars = {
        "bar_thickness": win_size[1] * 0.05,
        "sprite_size": ((win_size[0] / 3) - (win_size[1] * 0.1)) / 4,
        "width_sidebar": win_size[0] / 3,
        "bottom_bar_loc": win_size[1] * 0.95,
        "black": (0, 0, 0),
        "num_of_rectangles": 3,
        "circle_size": ((win_size[0] * (2 / 3)) - (4 * win_size[1] * 0.05)) / 3,
        "space_between_circles": win_size[1] * 0.05
    }

    # todo: multiple colours loaded from levels file?
    colour_list = [[(52, 83, 97), (63, 172, 185), (116, 190, 109), (235, 223, 255)],
                   [(60, 38, 80), (233, 72, 137), (255, 121, 93), (255, 184, 88)],
                   [(46, 58, 83), (96, 155, 185), (216, 225, 246), (249, 175, 164)]]
    colour_list_circle = [
        ["Circles1/0.png", "Circles1/1.png", "Circles1/2.png", "Circles1/3.png", "Circles1/4.png", "Circles1/5.png",
         "Circles1/6.png", "Circles1/7.png", "Circles1/8.png"],
        ["Circles2/0.png", "Circles2/1.png", "Circles2/2.png", "Circles2/3.png", "Circles2/4.png", "Circles2/5.png",
         "Circles2/6.png", "Circles2/7.png", "Circles2/8.png"],
        ["Circles3/0.png", "Circles3/1.png", "Circles3/2.png", "Circles3/3.png", "Circles3/4.png", "Circles3/5.png",
         "Circles3/6.png", "Circles3/7.png", "Circles3/8.png"]]

    rect_sprite_list = pygame.sprite.Group()

    number_list_white = ["number white/1.png", "number white/2.png", "number white/3.png", "number white/4.png",
                         "number white/5.png",
                         "number white/6.png", "number white/7.png", "number white/8.png", "number white/9.png"]

    number_list_black = ["number black/1.png", "number black/2.png", "number black/3.png", "number black/4.png",
                         "number black/5.png",
                         "number black/6.png", "number black/7.png", "number black/8.png", "number black/9.png"]

    # todo: i should maybe find a better way to do this lol

    list_of_circle_sprites = [[], [], []]
    list_of_overlay_sprites = [[], [], []]
    list_of_number_sprites = [[], [], []]

    for number in range(0, 3):
        list_of_circle_sprites[number] = pygame.sprite.Group()
        list_of_overlay_sprites[number] = pygame.sprite.Group()
        list_of_number_sprites[number] = pygame.sprite.Group()

    # -----------------------------
    # Chris you can probably get away with grouping win_width, win_height, sidebar_width, bar_thickness into one tuple.
    # I'll probably also make a configurator for the settings that will return all of these as a ilist or tuple.
    # -----------------------------

    # displaying sprites
    rect_sprite_list = addSidebarSprites(rect_sprite_list, colour_list, win_vars)
    for number in range(0, 3):
        list_of_circle_sprites[number] = addCircleSprites(background_colour,
                                                          colour_list_circle, number_list_white, number_list_black,
                                                          list_of_circle_sprites[number],
                                                          list_of_overlay_sprites[number],
                                                          list_of_number_sprites[number],
                                                          win_vars, number)

    # number_sprites = addNumberSprites(win_vars, number_list_white, number_list_black, number_sprites, id)

    window.fill(background_colour)
    rect_sprite_list.draw(window)
    pygame.display.update()

    # running the game
    circles_visible = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                # rectangleEventHandler(event, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEWHEEL:
                if pygame.mouse.get_pos()[0] < win_vars["width_sidebar"]:
                    if event.y == -1:
                        for rect_sprite in rect_sprite_list:
                            rect_sprite.rect.y -= win_vars["bar_thickness"]
                            if DEBUG: print(rect_sprite.rect.y)
                        updateSprites(rect_sprite_list, window, win_size[1], win_vars)
                        pygame.display.flip()
                    else:
                        for rect_sprite in rect_sprite_list:
                            rect_sprite.rect.y += win_vars["bar_thickness"]
                            if DEBUG: print(rect_sprite.rect.y)
                        updateSprites(rect_sprite_list, window, win_size[1], win_vars)
                        pygame.display.flip()

            # determines which rectangle is clicked?
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for rect_sprite in rect_sprite_list:
                        if rect_sprite.rect.collidepoint(pos):
                            rect_sprite.clicked = True
                            temp_id = rect_sprite.level_id
                            circles_visible = True
                            #print(temp_id)

            if circles_visible:
                pos = pygame.mouse.get_pos()
                for rect_sprite in list_of_overlay_sprites[temp_id]:
                    if rect_sprite.rect.collidepoint(pos) or rect_sprite.complete == True:
                        rect_sprite.hover = True
                        rect_sprite.fillImage(0)
                    else:
                        rect_sprite.hover = False
                        rect_sprite.fillImage(90)

                drawCircles(window, list_of_circle_sprites, temp_id)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for circle_sprite in list_of_circle_sprites[temp_id]:
                            if circle_sprite.rect.collidepoint(pos):
                                circle_sprite.clicked = True
                                #print(circle_sprite.pos_id)
                                test = runGame(temp_id, circle_sprite.pos_id)
                                print("this is runGame result", test)
                                # checking if level was completed
                                # chris this is not the rgiht way to do it just take the exist status.
                                # TODO: CURRENTLY THE LEVEL IS COUNTED AS COMPELTE ERVEN IF U CLOSE THE WINDOW --> TO FIX THIS I WILL MAKE A BUTTON INSTEAD AND UPON POUSHING THAT BUTTON TEST = 0 (AKA U FAILED)
                                # TODO: SO LIKE WE NEED TO FIND A WAY TO SAVE THE DATA OF WHICH LEVELS UVE COMPELTED RIGHTTT --> do u just write to a new file?
                                if (test == 0):
                                    print("won")
                                    for rect_sprite in list_of_overlay_sprites[temp_id]:
                                        if (rect_sprite.id == circle_sprite.list_id):
                                            rect_sprite.complete = True
                                    for number_sprite in list_of_number_sprites[temp_id]:
                                        if (number_sprite.id == circle_sprite.pos_id):
                                            print("updating")
                                            number_sprite.update_image(True)
                                            number_sprite.complete = True

                                pygame.display.set_caption("Gradient Rect")

                # circle_sprite_list.empty()
                window.fill(background_colour)
                drawCircles(window, list_of_circle_sprites, temp_id)
                draw(window, list_of_overlay_sprites[temp_id])
                draw(window, list_of_number_sprites[temp_id])
                rect_sprite_list.draw(window)

            pygame.display.flip()

    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !

# saving levels


if __name__ == "__main__":
    print("This is the main file!")
    sidebar()
    print("bleppers")
