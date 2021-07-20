# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

import sys
import pygame
from level import runGame
import sqlite3
from settings import settings
import numpy
from threading import Thread
import multiprocessing
import simpleaudio as sa

DEBUG = False


class Rect(pygame.sprite.Sprite):
    def __init__(self, sidebar_rect, x_pos, y_pos, level_id, win_vars):
        pygame.sprite.Sprite.__init__(self)
        self.size = int(win_vars["sidebar_rect_width"])
        self.image = pygame.transform.smoothscale(pygame.image.load(sidebar_rect[level_id]).convert_alpha(),
                                                  (self.size, int(self.size / 4)))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.level_id = level_id


class Circle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, win_vars, circle_list, i, j, pos_id, list_id):
        pygame.sprite.Sprite.__init__(self)
        self.size = int(win_vars["circle_size"])
        self.image = pygame.transform.smoothscale(pygame.image.load(circle_list[list_id][0][j]).convert_alpha(),
                                                  (self.size, self.size))
        self.image_dark = pygame.transform.smoothscale(pygame.image.load(circle_list[list_id][1][j]).convert_alpha(),
                                                       (self.size, self.size))
        self.image_light = pygame.transform.smoothscale(pygame.image.load(circle_list[list_id][0][j]).convert_alpha(),
                                                        (self.size, self.size))

        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.clicked = False
        self.has_been_clicked = False
        self.pos_id = pos_id  # pos id corresponds to the position of the thing on a level
        self.i = i
        self.j = j
        self.list_id = list_id  ## list id corresponds to the fucking LIST you put it ni you boNOBO
        # list ID currently corresponds to the STAGE or SET of colours.
        self.complete = False

    def update_image(self, bg):
        if bg == 0:
            self.image = self.image_light
        else:
            self.image = self.image_dark

        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


class OverlayNumbers(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, number_list, i, j, id, list_id, win_vars):
        pygame.sprite.Sprite.__init__(self)
        self.size = int(win_vars["circle_size"])

        self.image = pygame.transform.smoothscale(pygame.image.load(number_list[id]).convert_alpha(),
                                                  (self.size, self.size))
        self.img_blk = changeColour(pygame.transform.smoothscale(pygame.image.load(number_list[id]).convert_alpha(),
                                                                 (self.size, self.size)), 0, 0, 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.id = id
        self.i = i
        self.j = j
        self.list_id = list_id
        self.size = win_vars["circle_size"]
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
    def __init__(self, colour, win_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((win_size[0], win_size[1]))
        self.colour = colour
        self.image.set_alpha(0)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.open = False

    def fillWindow(self, alpha):
        self.image.set_alpha(alpha)
        self.image.fill(self.colour)

    def updateColour(self, colour):
        self.image.fill(colour)
        self.rect = self.image.get_rect()


def addSidebarSprites(sprite_list, win_vars, sidebar_rect):
    for i in range(0, win_vars["num_of_rectangles"]):
        sprite_list.add(Rect(sidebar_rect, win_vars["bar_thickness"],
                             (win_vars["bar_thickness"] * (i + 1)) + (win_vars["sprite_size"] * i), i, win_vars))

    return sprite_list


def addCircleSprites(background_colour, colour_list_circle, number_list, circle_sprites,
                     overlay_sprites, number_sprites, win_vars, level_id):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            circle_sprites.add(Circle((win_vars["width_sidebar"] + win_vars["bar_thickness"]) + j * (
                    win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars["bar_thickness"] + i * (
                                              win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars, colour_list_circle, i, count, count,
                                      level_id))  # OKAY SO I CHANGED THE FIRST COUNT FROM J TO COUNT it should work
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
                                              number_list, i, j, count, level_id, win_vars))
            count += 1

    return circle_sprites


def drawCircles(window, circle_sprites, id):
    circle_sprites[id].draw(window)


def draw(window, number_sprites):
    for sprite in number_sprites:
        window.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


def createDatabase():
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='levels' ''')

    if cur.fetchone()[0] != 1:
        cur.execute('''CREATE TABLE levels
                        (rect_id integer, circle_id integer, colour_codes text)''')
        cur.execute('''CREATE TABLE highscore
                        (rect_id integer, circle_id integer, score integer )''')
        cur.execute('''CREATE TABLE score
                        (rect_id integer, circle_id integer, score integer)''')
        cur.execute('''CREATE TABLE completedLevels
                        (rect_id integer, circle_id integer)''')
        cur.execute('''CREATE TABLE settings
                        (mode integer, cursor integer, size integer, adj integer, music integer)''')


def addSettingsToDatabase(mode, cursor, size, adj, music):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("INSERT INTO settings VALUES (:mode, :cursor, :size, :adj, :music)", (mode, cursor, size, adj, music))
    print("settings added")

    con.commit()


def getSettingsFromDatabase():
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM settings")

    score = cur.fetchone()
    print(score)

    return score


def isSavedSettings():
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM settings")
    data = cur.fetchall()
    if len(data) == 0:
        return 0
    else:
        return 1


def deleteSavedSettings():
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("DELETE from settings")

    con.commit()


def addLevelToDatabase(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("INSERT INTO completedLevels VALUES (:rect_id, :circle_id)", (rect_id, circle_id))

    con.commit()


def getLevelFromDatabase(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM completedLevels WHERE rect_id = :rect_id and circle_id = :circle_id",
                (rect_id, circle_id))
    data = cur.fetchall()
    if len(data) == 0:
        return 0
    else:
        return 1


def updateCompleteness(overlay_sprites, number_sprites):
    for i in range(3):
        for sprite in overlay_sprites[i]:
            if getLevelFromDatabase(i, sprite.id) == 1:
                sprite.complete = True
        for sprite in number_sprites[i]:
            if getLevelFromDatabase(i, sprite.id) == 1:
                sprite.update_image(True)
                sprite.complete = True


def changeColour(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue
    return surface


def splashscreen(win_size, window):
    done = False
    splashscreen = pygame.transform.smoothscale(
        pygame.image.load('Images/colour game splash screen.png').convert_alpha(), (win_size[0], win_size[1]))
    while not done:
        for event in pygame.event.get():
            window.blit(splashscreen, splashscreen.get_rect(topleft=(0, 0)))
            pygame.display.flip()
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                done = True


# This is the main entry point to the game.
def sidebar(windim, settingsOpen, settingColour, sidebarColour, cursor_value, mouse_adj, data, exit, showSplashscreen):
    # init

    win_size = windim
    done = False
    pygame.init()
    window = pygame.display.set_mode((win_size[0], win_size[1]), (pygame.RESIZABLE))
    pygame.display.set_caption("Shade of Hue")

    sidebar_colour = sidebarColour
    background_colour = settingColour

    # calculating variables
    win_vars = {
        "bar_thickness": win_size[1] * 0.05,
        "sidebar_rect_width": ((win_size[0] / 3) - (win_size[1] * 0.1)),
        "sprite_size": (((win_size[0] / 3) - (win_size[1] * 0.1))) / 4,
        "width_sidebar": win_size[0] / 3,
        "bottom_bar_loc": win_size[1] * 0.95,
        "black": (0, 0, 0),
        "num_of_rectangles": 6,
        "circle_size": ((win_size[0] * (2 / 3)) - (4 * win_size[1] * 0.05)) / 3,
        "space_between_circles": (win_size[1] * 0.05),
        "level_button_loc": (win_size[1]) / 2,
        "font_size": win_size[1] / 20,
        "gameboard_size": win_size[1],
        "exit_button_loc": (
            win_size[0] * 2 / 3 + ((((win_size[0] / 3) - (win_size[1] * 0.1))) / 6), win_size[1] * 3 / 4),
        "restart_button_loc": (win_size[0] - ((((win_size[0] / 3) - (win_size[1] * 0.1))) / 6) - (
                (((win_size[0] / 3) - (win_size[1] * 0.1))) / 4), win_size[1] * 3 / 4)

    }

    colour_list_circle = [
        [["Images/Circles1/0.png", "Images/Circles1/1.png", "Images/Circles1/2.png", "Images/Circles1/3.png",
          "Images/Circles1/4.png", "Images/Circles1/5.png",
          "Images/Circles1/6.png", "Images/Circles1/7.png", "Images/Circles1/8.png"],
         ["Images/Circles1Dark/0.png", "Images/Circles1Dark/1.png", "Images/Circles1Dark/2.png",
          "Images/Circles1Dark/3.png", "Images/Circles1Dark/4.png",
          "Images/Circles1Dark/5.png",
          "Images/Circles1Dark/6.png", "Images/Circles1Dark/7.png", "Images/Circles1Dark/8.png"]],
        [["Images/Circles2/0.png", "Images/Circles2/1.png", "Images/Circles2/2.png", "Images/Circles2/3.png",
          "Images/Circles2/4.png", "Images/Circles2/5.png",
          "Images/Circles2/6.png", "Images/Circles2/7.png", "Images/Circles2/8.png"],
         ["Images/Circles2Dark/0.png", "Images/Circles2Dark/1.png", "Images/Circles2Dark/2.png",
          "Images/Circles2Dark/3.png", "Images/Circles2Dark/4.png",
          "Images/Circles2Dark/5.png",
          "Images/Circles2Dark/6.png", "Images/Circles2Dark/7.png", "Images/Circles2Dark/8.png"]],
        [["Images/Circles3/0.png", "Images/Circles3/1.png", "Images/Circles3/2.png", "Images/Circles3/3.png",
          "Images/Circles3/4.png", "Images/Circles3/5.png",
          "Images/Circles3/6.png", "Images/Circles3/7.png", "Images/Circles3/8.png"],
         ["Images/Circles3Dark/0.png", "Images/Circles3Dark/1.png", "Images/Circles3Dark/2.png",
          "Images/Circles3Dark/3.png", "Images/Circles3Dark/4.png",
          "Images/Circles3Dark/5.png",
          "Images/Circles3Dark/6.png", "Images/Circles3Dark/7.png", "Images/Circles3Dark/8.png"]],
        [["Images/Circles4/0.png", "Images/Circles4/1.png", "Images/Circles4/2.png", "Images/Circles4/3.png",
          "Images/Circles4/4.png", "Images/Circles4/5.png",
          "Images/Circles4/6.png", "Images/Circles4/7.png", "Images/Circles4/8.png"],
         ["Images/Circles4Dark/0.png", "Images/Circles4Dark/1.png", "Images/Circles4Dark/2.png",
          "Images/Circles4Dark/3.png", "Images/Circles4Dark/4.png",
          "Images/Circles4Dark/5.png",
          "Images/Circles4Dark/6.png", "Images/Circles4Dark/7.png", "Images/Circles4Dark/8.png"]],
        [["Images/Circles6/0.png", "Images/Circles6/1.png", "Images/Circles6/2.png", "Images/Circles6/3.png",
          "Images/Circles6/4.png", "Images/Circles6/5.png",
          "Images/Circles6/6.png", "Images/Circles6/7.png", "Images/Circles6/8.png"],
         ["Images/Circles6Dark/0.png", "Images/Circles6Dark/1.png", "Images/Circles6Dark/2.png",
          "Images/Circles6Dark/3.png", "Images/Circles6Dark/4.png",
          "Images/Circles6Dark/5.png",
          "Images/Circles6Dark/6.png", "Images/Circles6Dark/7.png", "Images/Circles6Dark/8.png"]],
        [["Images/Circles5/0.png", "Images/Circles5/1.png", "Images/Circles5/2.png", "Images/Circles5/3.png",
          "Images/Circles5/4.png", "Images/Circles5/5.png",
          "Images/Circles5/6.png", "Images/Circles5/7.png", "Images/Circles5/8.png"],
         ["Images/Circles5Dark/0.png", "Images/Circles5Dark/1.png", "Images/Circles5Dark/2.png",
          "Images/Circles5Dark/3.png", "Images/Circles5Dark/4.png",
          "Images/Circles5Dark/5.png",
          "Images/Circles5Dark/6.png", "Images/Circles5Dark/7.png", "Images/Circles5Dark/8.png"]]
    ]

    rect_sprite_list = pygame.sprite.Group()

    number_list = ["Images/numberWhite/1.png", "Images/numberWhite/2.png", "Images/numberWhite/3.png",
                   "Images/numberWhite/4.png",
                   "Images/numberWhite/5.png", "Images/numberWhite/6.png", "Images/numberWhite/7.png",
                   "Images/numberWhite/8.png", "Images/numberWhite/9.png"]

    sidebar_rect = ["Images/sidebarRect/sidebar1.png", "Images/sidebarRect/sidebar2.png",
                    "Images/sidebarRect/sidebar3.png", "Images/sidebarRect/sidebar4.png",
                    "Images/sidebarRect/sidebar6.png", "Images/sidebarRect/sidebar5.png"]

    list_of_circle_sprites = []
    list_of_overlay_sprites = []
    list_of_number_sprites = []

    for number in range(0, win_vars["num_of_rectangles"]):
        list_of_circle_sprites.append(pygame.sprite.Group())
        list_of_overlay_sprites.append(pygame.sprite.Group())
        list_of_number_sprites.append(pygame.sprite.Group())

    # -----------------------------
    # Chris you can probably get away with grouping win_width, win_height, sidebar_width, bar_thickness into one tuple.
    # I'll probably also make a configurator for the settings that will return all of these as a ilist or tuple.
    # -----------------------------

    # displaying sprites
    rect_sprite_list = addSidebarSprites(rect_sprite_list, win_vars, sidebar_rect)
    for number in range(0, win_vars["num_of_rectangles"]):
        list_of_circle_sprites[number] = addCircleSprites(background_colour,
                                                          colour_list_circle, number_list,
                                                          list_of_circle_sprites[number],
                                                          list_of_overlay_sprites[number],
                                                          list_of_number_sprites[number],
                                                          win_vars, number)

    updateCompleteness(list_of_overlay_sprites, list_of_number_sprites)

    # init and setting variables
    circles_visible = False
    circles_has_been_clicked = False
    rect_can_be_clicked = True
    settingsPage = Settings(settingColour, win_size)
    settingsPage.open = settingsOpen
    settingsPage.colour = settingColour
    lmt, lmtc, dmt, dmtc = (0, 0, 0), (99, 85, 85), (255, 255, 255), (228, 217,
                                                                      201)  # lmt = lightmodetext, lmtc = lightmodetextonclick, dmt = darkmodetext, dmtc = darkmodetextonclick
    settingsButtonInvs = pygame.Rect(0, win_size[1] - int(win_vars["sprite_size"]), win_vars["sprite_size"],
                                     win_vars["sprite_size"])
    settingsButton = changeColour(pygame.transform.smoothscale(pygame.image.load("Images/settings.png").convert_alpha(),
                                                               (int(win_vars["sprite_size"] / 1.2),
                                                                int(win_vars["sprite_size"] / 1.2))), lmt[0], lmt[1],
                                  lmt[2])
    cursor_list = [pygame.image.load('Images/rsz_circle.png'), pygame.image.load('Images/rsz_x.png'),
                   pygame.image.load('Images/rsz_cursor.png')]
    cursor = cursor_value
    adj = mouse_adj

    mode = None

    textColour = lmt
    textClickedColour = lmtc

    windimPressed = False

    if showSplashscreen:
        done = splashscreen(win_size, window)

    # running the game
    while not done:
        if isSavedSettings():
            deleteSavedSettings()

        window.fill(background_colour)
        pygame.draw.rect(window, sidebar_colour, (0, 0, win_vars["width_sidebar"], win_size[1]))
        rect_sprite_list.draw(window)

        window.blit(settingsButton, (0, win_size[1] - int(win_vars["sprite_size"] / 1.2)))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                addSettingsToDatabase(mode, cursor, win_size[0], adj, data.value)
                print("saved data value is:", data.value)
                done = True
                data.value = 1
                exit.value = 1

            # determines which rectangle is clicked
            if settingsPage.open == True:
                circles_visible = False
                rect_can_be_clicked = False
                if circles_has_been_clicked == False:
                    temp_id = 0
                settingsPage.fillWindow(255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if settingsButtonInvs.collidepoint(
                            pos):  # todo: the invs thing is rlly messy i wanna fix if possible
                        settingsPage.open = True
                        circles_visible = False
                        rect_can_be_clicked = False
                        if circles_has_been_clicked == False:
                            temp_id = 0
                        settingsPage.fillWindow(255)
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
                                test = 2
                                while test == 2:
                                    print("restart")
                                    test = runGame(temp_id, circle_sprite.pos_id, cursor, background_colour, textColour,
                                                   textClickedColour, adj, win_vars, win_size)
                                    if (test == 0):
                                        for rect_sprite in list_of_overlay_sprites[temp_id]:
                                            if (rect_sprite.id == circle_sprite.pos_id):
                                                rect_sprite.complete = True
                                                addLevelToDatabase(temp_id, circle_sprite.pos_id)
                                        for number_sprite in list_of_number_sprites[temp_id]:
                                            if (number_sprite.id == circle_sprite.pos_id):
                                                number_sprite.update_image(True)
                                                number_sprite.complete = True

                                pygame.display.set_caption("Gradient Rect")

                window.fill(background_colour)
                pygame.draw.rect(window, sidebar_colour, (0, 0, win_vars["width_sidebar"], win_size[1]))
                drawCircles(window, list_of_circle_sprites, temp_id)
                draw(window, list_of_overlay_sprites[temp_id])
                draw(window, list_of_number_sprites[temp_id])
                rect_sprite_list.draw(window)
                window.blit(settingsButton, (0, win_size[1] - int(win_vars["sprite_size"] / 1.2)))

            if settingsPage.open:
                settingsPage.colour, background_colour, sidebar_colour, cursor, adj, win_size, circles_visible, rect_can_be_clicked, windimPressed = settings(
                    win_vars, cursor,
                    textClickedColour,
                    textColour,
                    settingsPage.colour,
                    sidebar_colour,
                    window, event, adj,
                    win_size,
                    settingsPage,
                    circles_visible,
                    rect_can_be_clicked,
                    cursor_list, lmt,
                    lmtc, dmt, dmtc, data)

            if background_colour == (255, 244, 234):
                mode = 0
            else:
                mode = 1

            if settingsPage.colour == (255, 244, 234):
                textColour = lmt
                textClickedColour = lmtc
            else:
                textColour = dmt
                textClickedColour = dmtc
            settingsButton = changeColour(settingsButton, textColour[0], textColour[1], textColour[2])
            for i in range(win_vars["num_of_rectangles"]):
                for sprite in list_of_overlay_sprites[i]:
                    sprite.colour = settingsPage.colour

            for i in range(win_vars["num_of_rectangles"]):
                for sprite in list_of_circle_sprites[i]:
                    sprite.update_image(mode)

            if windimPressed == True:
                sidebar(win_size, True, background_colour, sidebar_colour, cursor, adj, data, exit, False)
            pygame.mouse.set_visible(False)
            window.blit(cursor_list[cursor], (pygame.mouse.get_pos()[0] - adj, pygame.mouse.get_pos()[1] - adj))

            pygame.display.flip()

    pygame.quit()


def run_all(data, exit):
    print("This is the main file!")
    createDatabase()
    winsize = (600, 400)
    test = None
    backgroundColour = (255, 244, 234)
    sidebarColour = (235, 238, 211)
    cursor = 0
    adj = 10

    if isSavedSettings():
        test = getSettingsFromDatabase()
        winsize = (int(test[2]), int(test[2] * (2 / 3)))
        cursor = test[1]
        adj = test[3]
        data.value = int(test[4])
        if data.value == 10:
            data.value = 1

        if test[0] == 1:
            backgroundColour = (71, 60, 68)
            sidebarColour = (55, 51, 60)
        print(winsize, cursor, adj)
    print("data value from settings is:", data.value)
    sidebar(winsize, False, backgroundColour, sidebarColour, cursor, adj, data, exit, True)

    data.value = 1
    exit.value = 1


def play_sound():
    sa.WaveObject.from_wave_file('music.wav').play().wait_done()


if __name__ == "__main__":
    run_all()
