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
        self.level_id = level_id


class Circle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, win_vars, circle_list, j, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(circle_list[id][j]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.id = id


class Overlay(pygame.sprite.Sprite):
    # overlay is a really bad name but that's ok we will go with it
    def __init__(self, colour, x_pos, y_pos, win_vars, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((win_vars["circle_size"], win_vars["circle_size"]))
        self.alpha = 128
        self.image.set_alpha(128)
        self._original_colour = colour
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.hover = False
        self.clicked = False
        self.id = id

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


def addCircleSprites(colour_list_circle, circle_sprites, overlay_sprites, win_vars, id):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            circle_sprites.add(Circle((win_vars["width_sidebar"] + win_vars["bar_thickness"]) + i * (
                    win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars["bar_thickness"] + j * (
                                              win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars, colour_list_circle, count, id))
            overlay_sprites.add(Overlay((0, 0, 0),
                                        (win_vars["width_sidebar"] + win_vars["bar_thickness"]) + i * (
                                                win_vars["circle_size"] + win_vars["space_between_circles"]),
                                        win_vars["bar_thickness"] + j * (
                                                win_vars["circle_size"] + win_vars["space_between_circles"]),
                                        win_vars, id))
            count += 1

    return circle_sprites


# no longer drawing ellipses on top of sprites, its just drawing the sprites --> id is which rectangle was clicked so what colours to draw
def drawCircles(window, circle_sprites, colour_circle_list, id):
    circle_sprites[id].draw(window)


def drawOverlay(window, overlay_sprites):
    for sprite in overlay_sprites:
        window.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


def loadCircles(circle_list, win_vars):
    loaded_circle_list = []
    count = 0
    for circle in circle_list:
        loaded_circle_list.append(pygame.image.load(circle_list[0][count]))
        count += 1
    return loaded_circle_list


# This is the main entry point to the game.

def sidebar():
    # todo: anni will create a proper init function to set these variables.
    # init
    win_size = 600, 400
    done = False
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
    colour_list = [[(52, 83, 97), (63,172,185), (140, 224, 160), (199, 170, 237)],
                   [(60, 38, 80), (233, 72, 137), (255,121,93), (255,184,88)],
                   [(46,58,83), (96,155,185), (216,225,246), (249,175,164)]]
    colour_list_circle = [
        ["Circles1/0.png", "Circles1/1.png", "Circles1/2.png", "Circles1/3.png", "Circles1/4.png", "Circles1/5.png",
         "Circles1/6.png", "Circles1/7.png", "Circles1/8.png"],
        ["Circles2/0.png", "Circles2/1.png", "Circles2/2.png", "Circles2/3.png", "Circles2/4.png", "Circles2/5.png",
         "Circles2/6.png", "Circles2/7.png", "Circles2/8.png"],
        ["Circles3/0.png", "Circles3/1.png", "Circles3/2.png", "Circles3/3.png", "Circles3/4.png", "Circles3/5.png",
         "Circles3/6.png", "Circles3/7.png", "Circles3/8.png"]]
    rect_sprite_list = pygame.sprite.Group()
    circle_sprite_list0 = pygame.sprite.Group()
    circle_sprite_list1 = pygame.sprite.Group()
    circle_sprite_list2 = pygame.sprite.Group()

    listtt = [circle_sprite_list0, circle_sprite_list1, circle_sprite_list2]
    overlay_sprites = pygame.sprite.Group()

    # -----------------------------
    # Chris you can probably get away with grouping win_width, win_height, sidebar_width, bar_thickness into one tuple.
    # I'll probably also make a configurator for the settings that will return all of these as a list or tuple.
    # -----------------------------

    # displaying sprites
    rect_sprite_list = addSidebarSprites(rect_sprite_list, colour_list, win_vars)
    for number in range(0, 3):
        listtt[number] = addCircleSprites(colour_list_circle, listtt[number], overlay_sprites, win_vars, number)
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
                            # rect_sprite.clicked = False
                            # for sprite in overlay_sprites:
                            #     sprite.id = temp_id

            pos = pygame.mouse.get_pos()
            for rect_sprite in overlay_sprites:
                if rect_sprite.rect.collidepoint(pos):
                    rect_sprite.hover = True
                    rect_sprite.fillImage(0)
                else:
                    rect_sprite.hover = False
                    rect_sprite.fillImage(60)

            if circles_visible:
                drawCircles(window, listtt, colour_list_circle, temp_id)
                # circle_sprite_list.empty()
            drawOverlay(window, overlay_sprites)

            pygame.display.flip()

    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")
    sidebar()
    print("bleppers")
