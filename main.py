# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import random
import pygame
from level import runGame
import sqlite3

DEBUG = False


# todo: BIG BRAINED THINGS SO I DONT FORGET
# diff num of squares (4x4, 8x8, 10x10)
# find some way to show the difficulty of each level
# one the side of each lvl --> #moves, home, restart --> smth smth import the shuffle function or wtv


# class Rect(pygame.sprite.Sprite):
#     def __init__(self, x_pos, y_pos, colour, win_vars, level_id):
#         pygame.sprite.Sprite.__init__(self)
#
#         # todo: this surface needs to scale wrt window size. (checkmark)
#         self.image = pygame.Surface([win_vars["sprite_size"], win_vars["sprite_size"]])
#         self.image.fill(colour)
#         self.clicked = False
#         self.rect = self.image.get_rect()
#         self.rect.x = x_pos
#         self.rect.y = y_pos
#         # self.colour = colour
#         self.level_id = level_id  ## what the fuck is level id chris?!?

class Rect(pygame.sprite.Sprite):
    def __init__(self, sidebar_rect, x_pos, y_pos, level_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sidebar_rect[level_id]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.level_id = level_id


class Circle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, win_vars, circle_list, i, j, pos_id, list_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(circle_list[list_id][j]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.has_been_clicked = False
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

class Settings(pygame.sprite.Sprite):
    def __init__(self, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((600,400))
        self.colour = colour
        self.image.set_alpha(0)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.open = False

    def fillWindow(self, alpha):
        self.image.set_alpha(alpha)
        self.image.fill(self.colour)

    def updateColour(self):
        self.image = pygame.Surface((600,400))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()


# class Buttons(pygame.sprite.Sprite):
#     def __init(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.light_mode = pygame.Rect(40,40,160,40)
#         self.dark_mode = pygame.Rect(40, 100, 160, 40)
#         self.colour = (255,255,255)
#         self.rect

def createButtons():
    light_mode = pygame.Rect(40, 40, 160, 40)
    dark_mode = pygame.Rect(40, 100, 160, 40)
    return light_mode, dark_mode

#todo: I FUCKED THIS UP SO BADLY OMG its all wrong y i k e s


'''
OKAY SO many things to do, first we should create another class and then like in that other class we yeet in images from an array that i havent made yet
so like each button thing in the settings is an image (we need a clicked and not clicked version)
and then we do like if settingspage.open == true then we do all the collide point things and also change opacity of all the images to 255
otherwise we just like dont show them and dont allow ppl to press on them by yeeting it out of the if statement or wtv
    -> we would wanna do smth like a forloop to loop through all the possibilities and then we do a like if the clicked on this then this else if this then that
'''

   # def closeWindow(self):




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


def addSidebarSprites(sprite_list, colour_list, win_vars, sidebar_rect):
    for i in range(0, win_vars["num_of_rectangles"]):
        # for j in range(0, 4):
        #     sprite_list.add(
        #         Rect(win_vars["bar_thickness"] + (win_vars["sprite_size"] * j),
        #              (win_vars["bar_thickness"] * (i + 1)) + (win_vars["sprite_size"] * i), colour_list[i][j],
        #              win_vars, i))
        sprite_list.add(Rect(sidebar_rect, win_vars["bar_thickness"], (win_vars["bar_thickness"] * (i + 1)) + (win_vars["sprite_size"] * i), i))
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

def createDatabase():
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='levels' ''')

    if cur.fetchone()[0] != 1 :
        cur.execute('''CREATE TABLE levels
                        (rect_id integer, circle_id integer, colour_codes text)''')
        cur.execute('''CREATE TABLE highscore
                        (rect_id integer, circle_id integer, score integer )''')
        cur.execute('''CREATE TABLE score
                        (rect_id integer, circle_id integer, score integer)''')
        cur.execute('''CREATE TABLE completedLevels
                        (rect_id integer, circle_id integer)''')

        #print ("database has been created")

def addToDatabase(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("INSERT INTO completedLevels VALUES (:rect_id, :circle_id)", (rect_id, circle_id))

    con.commit()

def getFromDatabase(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM completedLevels WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))
    data = cur.fetchall()
    if len(data) == 0:
        return 0
    else:
        return 1

def updateCompleteness(overlay_sprites, number_sprites):
    for i in range (3):
        for sprite in overlay_sprites[i]:
            if getFromDatabase(i, sprite.id) == 1:
                sprite.complete = True
        for sprite in number_sprites[i]:
            if getFromDatabase(i, sprite.id) == 1:
                sprite.update_image(True)
                sprite.complete = True

def modes(lightMode, darkMode, textHoverColour, textColour, settingColour, sidebarColour, window, event):
    pos = pygame.mouse.get_pos()
    backgroundColour = settingColour
    sideColour = sidebarColour
    pygame.draw.rect(window, textColour, lightMode)
    pygame.draw.rect(window, textColour, darkMode)

    if lightMode.collidepoint(pos):
        pygame.draw.rect(window, textHoverColour, lightMode)
    if darkMode.collidepoint(pos):
        pygame.draw.rect(window, textHoverColour, darkMode)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if lightMode.collidepoint(pos):
            backgroundColour = (255, 244, 234)
            sideColour = (235, 238, 211)

        if darkMode.collidepoint(pos):
            backgroundColour = (71,60,68)
            sideColour = (55,51,60)

    return backgroundColour, backgroundColour, sideColour


# This is the main entry point to the game.

def sidebar():
    # todo: anni will create a proper init function to set these variables.
    # init
    win_size = 600, 400
    done = False
    # these are the light colours!
    sidebar_colour = (235,238,211)
    background_colour = (255,244,234)

    # these are the dark colours
    # sidebar_colour = (55,51,60)
    # background_colour = (71,60,68)


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
        ["Circles1NEW2/0.png", "Circles1NEW2/1.png", "Circles1NEW2/2.png", "Circles1NEW2/3.png", "Circles1NEW2/4.png", "Circles1NEW2/5.png",
         "Circles1NEW2/6.png", "Circles1NEW2/7.png", "Circles1NEW2/8.png"],
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

    sidebar_rect = ["sidebar rect with text/sidebar1.png", "sidebar rect with text/sidebar2.png", "sidebar rect with text/sidebar3.png"]

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
    rect_sprite_list = addSidebarSprites(rect_sprite_list, colour_list, win_vars, sidebar_rect)
    for number in range(0, 3):
        list_of_circle_sprites[number] = addCircleSprites(background_colour,
                                                          colour_list_circle, number_list_white, number_list_black,
                                                          list_of_circle_sprites[number],
                                                          list_of_overlay_sprites[number],
                                                          list_of_number_sprites[number],
                                                          win_vars, number)

    updateCompleteness(list_of_overlay_sprites, list_of_number_sprites)
    # number_sprites = addNumberSprites(win_vars, number_list_white, number_list_black, number_sprites, id)

    window.fill(background_colour)
    pygame.draw.rect(window, sidebar_colour, (0,0,200,400))
    rect_sprite_list.draw(window)
    settingsButtonInvs = pygame.Rect(0, 360,40,40)
    settingsCloseButtonInvs = pygame.Rect(0,0,40,40)
    settingsButton = pygame.image.load("rsz_gear-settings-icon-1.png").convert_alpha()
    window.blit(settingsButton, (0, 360))
    settingColour = (255, 244, 234)
    light, dark = createButtons()
    lmt, lmtc, dmt, dmtc = (0,0,0), (99,85,85), (255,255,255), (228,217,201) #lmt = lightmodetext, lmtc = lightmodetextonclick, dmt = darkmodetext, dmtc = darkmodetextonclick
    settingsPage = Settings(settingColour)

    pygame.display.update()

    # running the game
    circles_visible = False
    circles_has_been_clicked = False
    rect_can_be_clicked = True

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                # rectangleEventHandler(event, pygame.mouse.get_pos())
            # if event.type == pygame.MOUSEWHEEL:
            #     if pygame.mouse.get_pos()[0] < win_vars["width_sidebar"]:
            #         if event.y == -1:
            #             for rect_sprite in rect_sprite_list:
            #                 rect_sprite.rect.y -= win_vars["bar_thickness"]
            #                 if DEBUG: print(rect_sprite.rect.y)
            #             updateSprites(rect_sprite_list, window, win_size[1], win_vars)
            #             pygame.display.flip()
            #         else:
            #             for rect_sprite in rect_sprite_list:
            #                 rect_sprite.rect.y += win_vars["bar_thickness"]
            #                 if DEBUG: print(rect_sprite.rect.y)
            #             updateSprites(rect_sprite_list, window, win_size[1], win_vars)
            #             pygame.display.flip()

            # determines which rectangle is clicked?
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if settingsButtonInvs.collidepoint(pos):
                        settingsPage.open = True
                        circles_visible = False
                        rect_can_be_clicked = False
                        if circles_has_been_clicked == False:
                            temp_id = 0
                        settingsPage.fillWindow(255)
                    if settingsCloseButtonInvs.collidepoint(pos):
                        settingsPage.open = False
                        circles_visible = True
                        rect_can_be_clicked = True
                        settingsPage.fillWindow(0)
                    if rect_can_be_clicked == True:
                        for rect_sprite in rect_sprite_list:
                            if rect_sprite.rect.collidepoint(pos):
                                rect_sprite.clicked = True
                                temp_id = rect_sprite.level_id
                                circles_visible = True
                                circles_has_been_clicked = True

            if circles_visible:
                pos = pygame.mouse.get_pos()
                for rect_sprite in list_of_overlay_sprites[temp_id]:
                    if rect_sprite.rect.collidepoint(pos) or rect_sprite.complete == True:
                        rect_sprite.hover = True
                        rect_sprite.fillImage(0)
                    else:
                        rect_sprite.hover = False
                        rect_sprite.fillImage(70)

                drawCircles(window, list_of_circle_sprites, temp_id)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for circle_sprite in list_of_circle_sprites[temp_id]:
                            if circle_sprite.rect.collidepoint(pos):
                                circle_sprite.clicked = True
                                #print(circle_sprite.pos_id)
                                test = runGame(temp_id, circle_sprite.pos_id)
                                #print("this is runGame result", test)
                                # checking if level was completed
                                # chris this is not the rgiht way to do it just take the exist status.
                                # TODO: SO LIKE WE NEED TO FIND A WAY TO SAVE THE DATA OF WHICH LEVELS UVE COMPELTED RIGHTTT --> do u just write to a new file?
                                if (test == 0):
                                    # print("won")
                                    for rect_sprite in list_of_overlay_sprites[temp_id]:
                                        if (rect_sprite.id == circle_sprite.pos_id):
                                            rect_sprite.complete = True
                                            # print (temp_id, " and ", circle_sprite.pos_id)
                                            addToDatabase(temp_id, circle_sprite.pos_id)
                                    for number_sprite in list_of_number_sprites[temp_id]:
                                        if (number_sprite.id == circle_sprite.pos_id):
                                            # print("updating")
                                            number_sprite.update_image(True)
                                            number_sprite.complete = True

                                pygame.display.set_caption("Gradient Rect")

                # circle_sprite_list.empty()
                window.fill(background_colour)
                pygame.draw.rect(window, sidebar_colour, (0, 0, 200, 400))
                drawCircles(window, list_of_circle_sprites, temp_id)
                draw(window, list_of_overlay_sprites[temp_id])
                draw(window, list_of_number_sprites[temp_id])
                rect_sprite_list.draw(window)
                window.blit(settingsButton, (0, 360))

            textColour = None
            textClickedColour = None
            if settingsPage.open:
                if settingsPage.colour == (255,244,234):
                    textColour = lmt
                    textClickedColour = lmtc
                else:
                    textColour = dmt
                    textClickedColour = dmtc

                window.blit(settingsPage.image, (0, 0, 600, 400))
                settingsPage.colour, background_colour, sidebar_colour = modes(light, dark, textClickedColour, textColour, settingsPage.colour, sidebar_colour, window, event)
                settingsPage.updateColour()

            pygame.display.flip()

    pygame.quit()


# create loading screen!

# create level selection screen !

# create configuration screen !

# saving levels


if __name__ == "__main__":
    print("This is the main file!")
    createDatabase()
    sidebar()
    print("bleppers")
