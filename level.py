# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

# This describes the function of one level

import sys
import random
import pygame
import sqlite3
import math

# global vars
DEBUG = False


# Temp utils
# TODO: remove these
def drawGridLoose(window, win_size, steps, grid):
    x_size, y_size = win_size
    x_step, y_step = steps

    x_loc_scalar = x_size / x_step
    y_loc_scalar = y_size / y_step

    for x in range(0, x_step):
        for y in range(0, y_step):
            pygame.draw.rect(window, grid[x][y], (x * x_loc_scalar, y * y_loc_scalar, x_loc_scalar, y_loc_scalar))
    pygame.display.update()


def getColours(window, win_size, steps):
    x_size, y_size = win_size
    x_step, y_step = steps

    x_loc_scalar = x_size / x_step
    y_loc_scalar = y_size / y_step

    grid = []

    for x in range(0, x_step):
        templist = []
        for y in range(0, y_step):
            templist.append(pygame.Surface.get_at(window, (int(x * x_loc_scalar), int(y * y_loc_scalar))))
        grid.append(templist)
    return grid


# Const functions here.

class Rect(pygame.sprite.Sprite):
    def __init__(self, pos, colour, win_size, steps, constant=False):
        pygame.sprite.Sprite.__init__(self)
        rectsize_x = win_size[0] / steps[0]
        rectsize_y = win_size[1] / steps[1]
        self.image = pygame.Surface([rectsize_x, rectsize_y])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.original_x, self.original_y = pos
        self.colour = colour
        self.constant = constant

        if constant:
            self.movable = False
        else:
            self.movable = True


class Grid:
    """
    This class should contain (one) grid which we can use to control everything on each level
    """

    def __init__(self, window, colours, colour_size, constants, win_size, drawing_size, steps):
        self.window = window  # window which everything will be drawn onto
        self.colours = colours  # colours and their locations.
        self.gradient_size = colour_size
        self.constants = constants
        self.win_size = win_size  # (x, y) size of window
        self.drawing_size = drawing_size
        self.horizontal_limit = (2 / 3) * win_size[0]
        self.steps = steps
        self.original_grid = []
        self.shuffle_grid = []

    def drawGradient(self):
        x_size, y_size = self.drawing_size
        target_rect = pygame.Rect(0, 0, x_size, y_size)
        colour_rect = pygame.Surface(self.gradient_size)
        for i in self.colours:
            pygame.draw.line(colour_rect, i[0], i[1], i[1])
        colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
        self.window.blit(colour_rect, target_rect)
        pygame.display.update()

    def getColours(self, newgrid=False, ret=False):
        x_size, y_size = self.drawing_size
        x_step, y_step = self.steps

        x_loc_scalar = x_size / x_step
        y_loc_scalar = y_size / y_step

        if newgrid:
            for x in range(0, x_step):
                templist = []
                for y in range(0, y_step):
                    templist.append(pygame.Surface.get_at(self.window, (int(x * x_loc_scalar), int(y * y_loc_scalar))))
                self.new_grid.append(templist)
            if ret:
                return self.new_grid
        else:
            for x in range(0, x_step):
                templist = []
                for y in range(0, y_step):
                    templist.append(pygame.Surface.get_at(self.window, (int(x * x_loc_scalar), int(y * y_loc_scalar))))
                self.original_grid.append(templist)
            if ret:
                return self.newgrid

    def getGridColours(self):
        x_size, y_size = self.drawing_size
        x_step, y_step = self.steps

        x_loc_scalar = x_size / x_step
        y_loc_scalar = y_size / y_step

        templist = []

        for x in range(0, x_step):
            for y in range(0, y_step):
                templist.append(pygame.Surface.get_at(self.window, (int(x * x_loc_scalar), int(y * y_loc_scalar))))
            self.original_grid.append(templist)

        return templist

    def setColoursFromSaved(self, colourList):
        self.shuffle_grid = colourList
        if DEBUG: print (self.shuffle_grid)


    def shuffle(self, bypass=False):
        # if you want to bypass grid shuffling
        if bypass:
            self.shuffle_grid = self.original_grid


        x_step, y_step = self.steps
        templist = []
        for x in range(0, x_step):
            for y in range(0, y_step):
                if (x, y) in self.constants:
                    continue
                else:
                    templist.append(self.original_grid[x][y])

        random.shuffle(templist)

        count = 0
        for x in range(0, x_step):
            shuffleList = []
            for y in range(0, y_step):
                if (x, y) in self.constants:
                    shuffleList.append(self.original_grid[x][y])
                else:
                    shuffleList.append(templist[count])
                    count += 1
            self.shuffle_grid.append(shuffleList)

    def addToSpriteGroup(self, sprite_list):
        count = 0
        winx, winy = self.drawing_size
        x_step, y_step = self.steps

        x_block_width = winx / x_step
        y_block_width = winy / y_step

        # add sprites with x, y, colour
        for i in range(0, x_step):
            x_loc = i * x_block_width
            for j in range(0, y_step):
                y_loc = j * y_block_width
                pos = x_loc, y_loc
                if DEBUG: print(pos)
                if DEBUG: print(x_step, y_step)
                if (i, j) in self.constants:
                    if DEBUG: print("addToSpriteGroup constant: ", x_step, y_step)
                    rect = Rect(pos, self.shuffle_grid[i][j], self.drawing_size, self.steps, True)
                else:
                    rect = Rect(pos, self.shuffle_grid[i][j], self.drawing_size, self.steps)
                sprite_list.add(rect)
                # self.sprite_list.add(Rect(pos, self.shuffle_grid[i][j], self.win_size, self.steps))


def addColours(colour_list, rect_clicked, circle_clicked):
    colour = []
    for i in range(0, 4):
        colour.append(colour_list[rect_clicked][circle_clicked][i])
    return colour

def toString(colourList):

    string = "".join([str(element) for element in colourList])
    string = string.replace('(' , ', ')
    string = string.replace(')' , '')
    string = string[2:]
    string = string.replace(' ' , '')
    string = string.replace(',', ' ')
    return string

def toPygameColour(stringColours, steps):
    colourSplit = stringColours.split()
    colourList = []
    colourListSmall = []
    count = 0

    for i in range (int(math.sqrt(len(colourSplit)/4))):
        colourList.append([])
        for j in range (steps):
            for k in range (4):
                colourListSmall.append(int(colourSplit[count]))
                count += 1

            colourListSmall = tuple(colourListSmall)
            colourList[i].append(colourListSmall)
            colourListSmall = []

    if DEBUG: (colourList)
    return colourList



def getSavedColours(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM levels WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))

    level = cur.fetchone()
    return level[2]

def getSavedScore(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM score WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))

    score = cur.fetchone()
    return score[2]

def getHighScore(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM highscore WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))

    score = cur.fetchone()
    return score[2]

def saveLevel(rect_id, circle_id, colour_codes, count):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("INSERT INTO levels VALUES (:rect_id, :circle_id, :colour_codes)", (rect_id, circle_id, colour_codes))
    cur.execute("INSERT INTO score VALUES (:rect_id, :circle_id, :score)", (rect_id, circle_id, count))


    con.commit()

def deleteLevel(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()

    cur.execute("DELETE from levels where rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))
    cur.execute("DELETE from score where rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))

    con.commit()

def isCompletedLevel(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM highscore WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))
    data = cur.fetchall()
    if len(data) == 0:
        return 0
    else:
        return 1

def isSavedLevel(rect_id, circle_id):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM levels WHERE rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))
    data = cur.fetchall()
    if len(data) == 0:
        if DEBUG: print('there is no saved game')
        return 0
    else:
        if DEBUG: print('there is a game saved')
        return 1

def currentScore(window, move_count, background_colour, textColour, win_vars):
    font = pygame.font.Font('Quicksand-Regular.ttf', int(win_vars["font_size"]))
    score = font.render(str(int(move_count)), True, (textColour), (background_colour))
    score_rect = score.get_rect()
    score_rect.center = (win_vars["width_sidebar"]*2 + win_vars["width_sidebar"]/2, win_vars["sprite_size"]*5)

    text = font.render("CURRENT SCORE", True, textColour, background_colour)
    text_rect = text.get_rect()
    text_rect.center = (win_vars["width_sidebar"]*2 + win_vars["width_sidebar"]/2, win_vars["sprite_size"]*4)

    window.blit(text, text_rect)
    window.blit(score, score_rect)

def highScore(window, best_moves, background_colour, textColour, win_vars):
    font = pygame.font.Font('Quicksand-Regular.ttf', int(win_vars["font_size"]))
    score = font.render(str(int(best_moves)), True, (textColour), (background_colour))
    score_rect = score.get_rect()
    score_rect.center = (win_vars["width_sidebar"]*2 + win_vars["width_sidebar"]/2, win_vars["sprite_size"]*2)

    text = font.render("HIGH SCORE", True, textColour, background_colour)
    text_rect = text.get_rect()
    text_rect.center = (win_vars["width_sidebar"] * 2 + win_vars["width_sidebar"] / 2, win_vars["sprite_size"])

    window.blit(text, text_rect)

    window.blit(score, score_rect)

def saveHighScore(rect_id, circle_id, new_score):
    con = sqlite3.connect('levels.db')
    cur = con.cursor()
    if isCompletedLevel(rect_id, circle_id) == 1:
        top_score = getHighScore(rect_id, circle_id)
    else:
        top_score = math.inf

    if new_score < top_score:
        cur.execute("DELETE from highscore where rect_id = :rect_id and circle_id = :circle_id", (rect_id, circle_id))
        cur.execute("INSERT INTO highscore VALUES (:rect_id, :circle_id, :score)", (rect_id, circle_id, new_score))

    con.commit()

def buttons(mode, win_vars, exit_buttons, restart_buttons, window):
    window.blit(exit_buttons[mode], win_vars["exit_button_loc"])
    window.blit(restart_buttons[mode], win_vars["restart_button_loc"])

    if exit_buttons[mode].get_rect(topleft = win_vars["exit_button_loc"]).collidepoint(pygame.mouse.get_pos()):
        window.blit(exit_buttons[mode+1], win_vars["exit_button_loc"])

    if restart_buttons[mode].get_rect(topleft = win_vars["restart_button_loc"]).collidepoint(pygame.mouse.get_pos()):
        window.blit(restart_buttons[mode+1], win_vars["restart_button_loc"])


def evaluate_level(window, levelgrid, sprite_list, rect_id, circle_id, move_count, cursor, background_colour, textColour, textClickedColour, adj, win_vars, hasHighScore, winsize):
    done = False
    moving_sprite_list = pygame.sprite.GroupSingle()
    clicked_sprite_list = pygame.sprite.GroupSingle()
    save_level_button = pygame.Rect(win_vars["width_sidebar"]*2+win_vars["sprite_size"]/2, win_vars["level_button_loc"], win_vars["sidebar_rect_width"],win_vars["sprite_size"])
    restart_level_button = pygame.Rect(win_vars["width_sidebar"]*2+win_vars["sprite_size"]/2, win_vars["level_button_loc"]+win_vars["sprite_size"]+win_vars["sprite_size"]/2, win_vars["sidebar_rect_width"], win_vars["sprite_size"])
    cursor_list = [pygame.image.load('rsz_circle.png'), pygame.image.load('rsz_x.png'), pygame.image.load('rsz_cursor.png')]

    exit_buttons = [pygame.image.load('exit/exit_dark.png'), pygame.image.load('exit/exit_dark_hover.png'), pygame.image.load('exit/exit_light.png'), pygame.image.load('exit/exit_light_hover.png')]
    restart_buttons = [pygame.image.load('restart/restart_dark.png'), pygame.image.load('restart/restart_dark_hover.png'), pygame.image.load('restart/restart_light.png'), pygame.image.load('restart/restart_light_hover.png')]
    exit_buttons = [pygame.transform.smoothscale(x, (int(win_vars["sprite_size"]),int(win_vars["sprite_size"]))) for x in exit_buttons]
    restart_buttons = [pygame.transform.smoothscale(x, (int(win_vars["sprite_size"]),int(win_vars["sprite_size"]))) for x in restart_buttons]

    mode = None

    if background_colour == (255,244,234):
        mode = 2
    else:
        mode = 0


    rect_size = win_vars["gameboard_size"]/10
    if circle_id < 3:
        rect_size = win_vars["gameboard_size"]/4
    elif circle_id < 6:
        rect_size = win_vars["gameboard_size"]/8

    show_cursor = True

    # TODO: THIS LIMIT NEEDS TO BE CHANGED TO BE A PASSED VAR TO RESPOND TO SCRREEN SCALING --> levelgrid.horizontalLimit **DONE I THINK**
    while not done:

        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     return 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                posx, posy = pos
                # Button to quit
                if exit_buttons[0].get_rect(topleft = win_vars["exit_button_loc"]).collidepoint(pos):
                    if DEBUG: print("white button pressed")
                    saveLevel(rect_id, circle_id, toString(levelgrid.getGridColours()), int(move_count)) #HOW TO CHANGE ARRAY INTO STRING WITHOUT ILELJAHFDKAGHFDK
                    if DEBUG: print ("getgridcolours", levelgrid.getGridColours())
                    if DEBUG: print ("getsavecolours", getSavedColours(rect_id, circle_id))
                    done = True
                if restart_buttons[mode].get_rect(topleft=win_vars["restart_button_loc"]).collidepoint(pos):
                    done = True
                    runGame(rect_id, circle_id, cursor, background_colour, textColour, textClickedColour, adj, win_vars, winsize)

                # if DEBUG: print("this is mousebutton down posx, posy: ", pos)
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(pos) and sprite.movable:
                        if DEBUG: print(sprite.constant)
                        sprite.clicked = True
                        moving_sprite_list.add(sprite)
                        clicked_sprite_list = moving_sprite_list.copy()

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if DEBUG: print("this is mousebutton up pos:", pos)
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(pos) and sprite.movable:
                        move_count += 0.5
                        for sprite2 in moving_sprite_list:
                            sprite.rect.x = sprite2.original_x
                            sprite.rect.y = sprite2.original_y
                            sprite2.rect.x = sprite.original_x
                            sprite2.rect.y = sprite.original_y
                            sprite.original_x = sprite.rect.x
                            sprite.original_y = sprite.rect.y
                            sprite2.original_x = sprite2.rect.x
                            sprite2.original_y = sprite2.rect.y
                    else:
                        sprite.rect.x = sprite.original_x
                        sprite.rect.y = sprite.original_y
                    sprite.clicked = False
                if move_count % 1 != 0:
                    move_count -= 0.5
                if DEBUG: print (int(move_count))


                moving_sprite_list.empty()
                clicked_sprite_list.empty()

            if event.type == pygame.MOUSEMOTION:
                posx, posy = pygame.mouse.get_pos()
                for sprite in moving_sprite_list:
                    # iirc the below code should run ok
                    if sprite.clicked == True and sprite.movable and (posx < levelgrid.horizontal_limit):
                        sprite.rect.move_ip(event.rel)

        #moving_sprite_list.draw(window)
        sprite_list.draw(window)  # THIS IS WHAT IS DRAWING THE SPRITES!
        moving_sprite_list.draw(window)  # draw this last ALWAYS

        # TODO: FIND A BETTER WAY TO DRAW RECTANGLES
        # in particular, we need a better way to calculate the '200' present here.
        pygame.draw.rect(window, (background_colour),
                         pygame.Rect(levelgrid.horizontal_limit, 0, levelgrid.horizontal_limit / 2,
                                     levelgrid.horizontal_limit))

        # # load = pygame.Rect(420,200,160,40)
        # # restart = pygame.Rect(420, 260, 160, 40)
        # if save_level_button.collidepoint(pygame.mouse.get_pos()):
        #     pygame.draw.rect(window, (textClickedColour), (save_level_button))  # THIS IS JUST A TEST THING :)
        # else:
        #     pygame.draw.rect(window, (textColour), (save_level_button))  # THIS IS JUST A TEST THING :)
        #
        # if restart_level_button.collidepoint(pygame.mouse.get_pos()):
        #     pygame.draw.rect(window, (textClickedColour), (restart_level_button))  # THIS IS JUST A TEST THING :)
        # else:
        #     pygame.draw.rect(window, (textColour), (restart_level_button))  # THIS IS JUST A TEST THING :)

        buttons(mode, win_vars, exit_buttons, restart_buttons, window)

        currentScore(window, move_count, background_colour, textColour, win_vars)
        if hasHighScore == 1:
            highScore(window, getHighScore(rect_id, circle_id), background_colour, textColour, win_vars)
        else:
            highScore(window, 0, background_colour, textColour, win_vars)

        pygame.mouse.set_visible(False)



        for sprite in moving_sprite_list:
            pygame.draw.rect(window, window.get_at((int(sprite.original_x), int(sprite.original_y))), (int(sprite.original_x), int(sprite.original_y), rect_size, rect_size))

        window.blit(cursor_list[cursor], ((pygame.mouse.get_pos()[0]-adj), (pygame.mouse.get_pos()[1]-adj)))




        '''
        todo: create a new button, when button is clicked, first run smth similar to the .getColour() method to yeet the data into a sql thing or a text file
        and then when u yeet the data back, aka when the level is clicked again, u run the .addToSpriteGroup() function to yeet it back
        idk how to create a database or file or wtv for each level HELP
        '''

        pygame.display.flip()

        if levelgrid.original_grid == getColours(window, (levelgrid.horizontal_limit, levelgrid.horizontal_limit),
                                                 levelgrid.steps):
            deleteLevel(rect_id, circle_id)
            saveHighScore(rect_id, circle_id, move_count)
            if DEBUG: print("you won")
            done = True  # important: we should need this but why dont we wghat
            return 0  # 0 = won the game
            # you've won the game


def run_level(level, rect_id, circle_id, cursor, background_colour, textColour, textClickedColour, adj, win_vars, winsize): #todo: ive alos gotta add rect id and circle id arguments here i think as well as in evaluate level g y u h
    """This will run the entire level!"""
    isComplete = 1
    # Todo: Do we want this to only run one level?
    # system level variables.
    sprite_list = pygame.sprite.Group()
    sprite_single = pygame.sprite.GroupSingle()

    window, colours, colour_size, constants, win_size, steps = level
    pygame.display.set_caption("LEVEL!!!!!")
    if win_size[0] < win_size[1]:
        drawing_size = (win_size[0], win_size[0])
    else:
        drawing_size = (win_size[1], win_size[1])

    # TODO: horizontal lim to be coded here with diff between drawing size and window sizes

    # pygame.init()  # is pygame already init from another side?
    # window = pygame.display.set_mode((win_size))
    levelgrid = Grid(window, colours, colour_size, constants, win_size, drawing_size, steps)
    if DEBUG: print(constants)

    levelgrid.drawGradient()
    # drawGridLoose(window, win_size, steps, levelgrid.shuffle_grid) # todo: remove
    levelgrid.getColours()
    levelgrid.shuffle(bypass = False)

    #todo: insert an if statement here checking if there is a game saved and if so just addtospritegroup and dont do everything else
    isLevelSaved = isSavedLevel(rect_id, circle_id)
    move_count = 0
    if isLevelSaved == 1:
        if DEBUG: print("steps:", levelgrid.steps[1])
        colourList = toPygameColour(getSavedColours(rect_id, circle_id), levelgrid.steps[0])
        if DEBUG: print ("getsavecolours", getSavedColours(rect_id, circle_id))
        levelgrid.setColoursFromSaved(colourList)
        move_count = getSavedScore(rect_id, circle_id)
        deleteLevel(rect_id, circle_id)

    levelgrid.addToSpriteGroup(sprite_list)

    hasHighScore = isCompletedLevel(rect_id, circle_id)

    if evaluate_level(window, levelgrid, sprite_list, rect_id, circle_id, move_count, cursor, background_colour, textColour, textClickedColour, adj, win_vars, hasHighScore, winsize) == 0:
        print("you have won")
        iscomplete = 0
    else:
        iscomplete = 1

    return iscomplete

    # sys.exit()

    # at this point, everything has been created properly, hand over to run_game.


def runGame(rect_id, circle_id, cursor, background_colour, textColour, textClickedColour, adj, win_vars, winsize):
    level = 0  # TODO: CHANGE THIS
    level_complete = 0
    win_size = winsize
    testWindow = pygame.display.set_mode((win_size))

    # common sizes for 1200x900
    # 300x300:  x=4     y=3
    # 150x150:  x=8     y=6
    # 100x100:  x=12    y=9
    # 75x75:    x=16    y=12
    # 60x60:    x=20    y=15
    # 50x50:    x=24    y=18

    # for 900x900, 9, 6, 3
    # steps = 8, 8

    # IDFK IF I CAN DO THIS BUT HAVE IT ANYWAYS
    # okay so pretty much [] is the whole list, [[colourlist]], [[[four colours]]] are nested inside and within
    # [[[four colours]]] there are [[[[colour1, pos], [colour2, pos], [colour3, pos], [colour4, pos]]]]

    colour_list = [
        # colourlist 1
        [[[(27, 74, 94), (0, 0)], [(55, 156, 147), (1, 0)],
          [(255, 226, 223), (0, 1)], [(223, 255, 235), (1, 1)]],
         [[(29, 74, 82), (0, 0)], [(239, 143, 149), (1, 0)],
          [(130, 202, 193), (0, 1)], [(255, 241, 242), (1, 1)]],
         [[(255, 168, 192), (0, 0)], [(255, 234, 237), (1, 0)],
          [(64, 99, 118), (0, 1)], [(69, 173, 157), (1, 1)]],
         [[(255, 248, 249), (0, 0)], [(255, 116, 151), (1, 0)],
          [(84, 176, 163), (0, 1)], [(10, 46, 65), (1, 1)]],
         [[(73, 166, 162), (0, 0)], [(218, 255, 194), (1, 0)],
          [(32, 58, 69), (0, 1)], [(255, 198, 205), (1, 1)]],
         [[(255, 168, 192), (0, 0)], [(255, 234, 237), (1, 0)],
          [(32, 78, 57), (0, 1)], [(111, 209, 193), (1, 1)]],
         [[(55, 130, 136), (0, 0)], [(255, 203, 205), (1, 0)],
          [(129, 219, 201), (0, 1)],[(218, 240, 199), (1, 1)]],
         [[(35, 95, 97), (0, 0)], [(160, 168, 151), (1, 0)],
          [(127, 239, 244), (0, 1)],[(255, 203, 219), (1, 1)]],
         [[(33, 115, 115), (0, 0)], [(141, 205, 137), (1, 0)],
          [(255, 226, 223), (0, 1)],[(223, 255, 235), (1, 1)]]],
        # colourlist 2
        [[[(211, 90, 63), (0, 1)], [(148, 41, 110), (1, 1)],
          [(118, 126, 154), (1, 0)], [(194, 119, 144), (0, 0)]],
         [[(105, 28, 144), (0, 1)], [(166, 126, 186), (1, 1)],
          [(255, 113, 123), (1, 0)], [(149, 16, 71), (0, 0)]],
         [[(148, 63, 140), (0, 1)], [(244, 221, 255), (1, 1)],
          [(255, 228, 234), (1, 0)], [(140, 3, 31), (0, 0)]],
         [[(180, 155, 255), (0, 1)], [(118, 24, 85), (1, 1)],
          [(255, 162, 79), (1, 0)], [(255, 207, 215), (0, 0)]],
         [[(245, 164, 188), (0, 1)], [(255, 208, 150), (1, 1)],
          [(255, 138, 133), (1, 0)], [(101, 12, 37), (0, 0)]],
         [[(255, 171, 110), (0, 1)], [(255, 46, 113), (1, 1)],
          [(194, 192, 255), (1, 0)], [(255, 244, 218), (0, 0)]],
         [[(255, 235, 235), (0, 1)], [(255, 189, 211), (1, 1)],
          [(227, 33, 139), (1, 0)], [(255, 104, 53), (0, 0)]],
         [[(249, 81, 160), (0, 1)], [(247, 220, 255), (1, 1)],
          [(255, 249, 223), (1, 0)], [(255, 117, 110), (0, 0)]],
         [[(255, 219, 209), (0, 1)], [(224, 85, 113), (1, 1)],
          [(255, 191, 99), (1, 0)], [(255, 243, 100), (0, 0)]]],
        # colourlist 3
        [[[(255, 195, 237), (0, 1)], [(227, 245, 255), (1, 1)],
          [(119, 209, 254), (1, 0)], [(92, 111, 125), (0, 0)]],
         [[(103, 109, 126), (0, 1)], [(255, 224, 131), (1, 1)],
          [(169, 185, 218), (1, 0)], [(72, 144, 166), (0, 0)]],
         [[(220, 231, 255), (0, 1)], [(101, 157, 224), (1, 1)],
          [(255, 216, 173), (1, 0)], [(54, 50, 65), (0, 0)]],
         [[(12, 32, 57), (0, 1)], [(86, 145, 214), (1, 1)],
          [(230, 242, 255), (1, 0)], [(249, 189, 153), (0, 0)]],
         [[(28, 34, 67), (0, 1)], [(3, 67, 81), (1, 1)],
          [(236, 236, 255), (1, 0)], [(255, 189, 180), (0, 0)]],
         [[(140, 212, 255), (0, 1)], [(34, 62, 103), (1, 1)],
          [(255, 144, 130), (1, 0)], [(222, 236, 255), (0, 0)]],
         [[(209, 223, 255), (0, 1)], [(70, 99, 180), (1, 1)],
          [(194, 136, 185), (1, 0)], [(255, 174, 147), (0, 0)]],
         [[(236, 245, 255), (0, 1)], [(169, 219, 255), (1, 1)],
          [(72, 83, 120), (1, 0)], [(255, 200, 199), (0, 0)]],
         [[(255, 158, 137), (0, 1)], [(72, 87, 105), (1, 1)],
          [(156, 192, 240), (1, 0)], [(166, 245, 255), (0, 0)]]],
        #colourlist 4 (really circles6)
        [[[(115, 223, 217), (0, 0)], [(255, 230, 148), (1, 0)], [(171, 142, 242), (0, 1)], [(254, 139, 158), (1, 1)]],
         [[(255, 201, 128), (0, 0)], [(72, 180, 194), (1, 0)], [(234, 161, 181), (0, 1)], [(199, 226, 255), (1, 1)]],
         [[(137, 205, 212), (0, 0)], [(255, 191, 168), (1, 0)], [(177, 243, 197), (0, 1)], [(249, 255, 181), (1, 1)]],
         [[(126, 213, 191), (0, 0)], [(220, 255, 209), (1, 0)], [(231, 166, 180), (0, 1)], [(255, 216, 168), (1, 1)]],
         [[(212, 164, 178), (0, 0)], [(127, 191, 231), (1, 0)], [(239, 229, 180), (0, 1)], [(178, 247, 200), (1, 1)]],
         [[(203, 170, 242), (0, 0)], [(134, 231, 240), (1, 0)], [(255, 207, 199), (0, 1)], [(255, 224, 181), (1, 1)]],
         [[(103, 197, 199), (0, 0)], [(186, 245, 231), (1, 0)], [(96, 119, 137), (0, 1)], [(235, 177, 180), (1, 1)]],
         [[(232, 196, 132), (0, 0)], [(252, 126, 138), (1, 0)], [(255, 199, 250), (0, 1)], [(161, 122, 222), (1, 1)]],
         [[(159, 213, 163), (0, 0)], [(99, 187, 196), (1, 0)], [(253, 201, 209), (0, 1)], [(116, 149, 208), (1, 1)]]],
        #colourlist 5 (really circles4)
        [[[(16, 19, 38), (0, 0)], [(137, 162, 193), (1, 0)],
          [(212, 195, 198), (0, 1)], [(227, 214, 209), (1, 1)]],
         [[(110, 152, 186), (0, 0)], [(61, 74, 91), (1, 0)],
          [(204, 220, 230), (0, 1)], [(247, 234, 222), (1, 1)]],
         [[(171, 159, 154), (0, 0)], [(45, 55, 71), (1, 0)],
          [(228, 236, 245), (0, 1)], [(149, 174, 202), (1, 1)]],
         [[(225, 238, 243), (0, 0)], [(207, 177, 142), (1, 0)],
          [(163, 189, 225), (0, 1)], [(63, 88, 126), (1, 1)]],
         [[(220, 236, 244), (0, 0)], [(203, 183, 186), (1, 0)],
          [(118, 165, 167), (0, 1)], [(63, 91, 126), (1, 1)]],
         [[(223, 238, 244), (0, 0)], [(170, 172, 211), (1, 0)],
          [(173, 204, 220), (0, 1)], [(63, 88, 126), (1, 1)]],
         [[(255, 247, 247), (0, 0)], [(213, 213, 232), (1, 0)],
          [(166, 201, 227), (0, 1)], [(84, 122, 141), (1, 1)]],
         [[(181, 199, 235), (0, 0)], [(81, 159, 196), (1, 0)],
          [(230, 233, 238), (0, 1)], [(191, 235, 255), (1, 1)]],
         [[(245, 249, 255), (0, 0)], [(240, 228, 228), (1, 0)],
          [(204, 197, 230), (0, 1)], [(121, 135, 189), (1, 1)]]],

    ]

    colours = addColours(colour_list, rect_id, circle_id)

    colour_size = (2, 2)
    # use 4 random colours for now
    # c1, c2, c3, c4 = ((33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69))
    # c1 = (255, 0, 0)
    # c2 = (0, 255, 0)
    # c3 = (0, 0, 255)
    # c4 = (150, 150, 150)

    # constants are blocks that won't move.

    # 7x7 block
    # constants.append((0, 0))
    # constants.append((6, 6))
    # constants.append((0, 6))
    # constants.append((6, 0))
    # constants.append((3, 3))

    # createColourGridyx(windowSize, c1, c2, c3, c4, x_step, y_step, constants)
    x_step = 10
    y_step = 10

    if (0 <= circle_id < 3):
        x_step = 4
        y_step = 4
    elif (3 <= circle_id < 6):
        x_step = 8
        y_step = 8

    steps = x_step, y_step
    # constants are blocks that won't move.
    constants = []

    # general block
    constants.append((0, 0))
    constants.append((x_step - 1, y_step - 1))
    constants.append((0, y_step - 1))
    constants.append((x_step - 1, 0))

    level = testWindow, colours, colour_size, constants, win_size, steps
    return run_level(level, rect_id, circle_id, cursor, background_colour, textColour, textClickedColour, adj, win_vars, winsize)


if __name__ == "__main__":
    level = 0  # TODO: CHANGE THIS
    win_size = (400, 400)
    testWindow = pygame.display.set_mode((win_size))
    pygame.display.set_caption("test_window")

    # common sizes for 1200x900
    # 300x300:  x=4     y=3
    # 150x150:  x=8     y=6
    # 100x100:  x=12    y=9
    # 75x75:    x=16    y=12
    # 60x60:    x=20    y=15
    # 50x50:    x=24    y=18

    # for 900x900, 9, 6, 3
    # steps = 8, 8
    steps = 4, 4
    x_step, y_step = steps
    colours = []
    # set 1
    # colours.append([(255, 153, 51),(1,1)])
    # colours.append([(153, 51, 255),(0,1)])
    # colours.append([(51, 153, 255),(0,0)])
    # colours.append([(51, 255, 153),(1,0)])

    # set 2
    # colours.append([(33, 11, 844), (0, 0)])
    # colours.append([(201, 205, 242), (0, 1)])
    # colours.append([(201, 255, 240), (1, 1)])
    # colours.append([(6, 39, 69), (1, 0)])

    # set 3
    # colours.append([(0, 17, 54), (0, 0)])
    # colours.append([(150, 255, 210), (0, 1)])
    # colours.append([(255, 255, 255), (0, 2)])
    # colours.append([(183, 78, 212), (1, 0)])
    # colours.append([(197, 181, 255), (1, 1)])
    # colours.append([(255, 229, 97), (1, 2)])
    # colours.append([(148, 0, 55), (2, 0)])
    # colours.append([(235, 115, 159), (2, 1)])
    # colours.append([(191, 244, 255), (2, 2)])

    # colours.append([(240,230,140),(1,0)])
    # colours.append([(129,0,0), (1,1)])

    # set 4
    colours.append([(255, 255, 255), (0, 0)])
    colours.append([(168, 220, 255), (0, 1)])
    colours.append([(0, 29, 69), (1, 1)])
    colours.append([(255, 171, 107), (1, 0)])

    # IDFK IF I CAN DO THIS BUT HAVE IT ANYWAYS
    # okay so pretty much [] is the whole list, [[four colours]] are nested inside and within [[four colours]] there are [[[colour1, pos], [colour2, pos], [colour3, pos], [colour4, pos]]]
    colour_list1 = [
        [[(51, 111, 84), (0, 1)], [(180, 239, 255), (1, 1)],
         [(90, 223, 92), (1, 0)], [(91, 112, 82), (0, 0)]],
        [[(84, 107, 78), (0, 1)], [(121, 154, 227), (1, 1)],
         [(40, 128, 104), (1, 0)], [(159, 237, 105), (0, 0)]],
        [[(161, 199, 255), (0, 1)], [(22, 61, 103), (1, 1)],
         [(41, 129, 105), (1, 0)], [(157, 237, 104), (0, 0)]],
        [[(160, 1247, 227), (0, 1)], [(226, 245, 255), (1, 1)],
         [(120, 209, 254), (1, 0)], [(30, 109, 81), (0, 0)]],
        [[(155, 136, 184), (0, 1)], [(125, 234, 163), (1, 1)],
         [(125, 234, 163), (1, 0)], [(225, 255, 225), (0, 0)]],
        [[(161, 199, 255), (0, 1)], [(41, 164, 186), (1, 1)],
         [(136, 191, 156), (1, 0)], [(166, 245, 255), (0, 0)]],
        [[(231, 255, 246), (0, 1)], [(99, 255, 211), (1, 1)],
         [(105, 183, 232), (1, 0)], [(180, 175, 239), (0, 0)]],
        [[(210, 223, 255), (0, 1)], [(70, 99, 180), (1, 1)],
         [(131, 236, 151), (1, 0)], [(38, 243, 182), (0, 0)]],
        [[(74, 79, 224), (0, 1)], [(247, 220, 255), (1, 1)],
         [(170, 255, 213), (1, 0)], [(50, 174, 213), (0, 0)]],
    ]

    colour_list2 = [
        [[(211, 90, 63), (0, 1)], [(148, 41, 110), (1, 1)],
         [(118, 126, 154), (1, 0)], [(194, 119, 144), (0, 0)]],
        [[(105, 28, 144), (0, 1)], [(166, 126, 186), (1, 1)],
         [(255, 113, 123), (1, 0)], [(149, 16, 71), (0, 0)]],
        [[(148, 63, 140), (0, 1)], [(244, 221, 255), (1, 1)],
         [(255, 228, 234), (1, 0)], [(140, 3, 31), (0, 0)]],
        [[(180, 155, 255), (0, 1)], [(118, 24, 85), (1, 1)],
         [(255, 207, 215), (1, 0)], [(255, 162, 79), (0, 0)]],
        [[(255, 214, 238), (0, 1)], [(255, 200, 129), (1, 1)],
         [(255, 138, 133), (1, 0)], [(101, 12, 37), (0, 0)]],
        [[(194, 192, 255), (0, 1)], [(255, 46, 113), (1, 1)],
         [(255, 244, 218), (1, 0)], [(249, 159, 93), (0, 0)]],
        [[(236, 200, 255), (0, 1)], [(255, 233, 248), (1, 1)],
         [(227, 33, 139), (1, 0)], [(255, 104, 53), (0, 0)]],
        [[(249, 81, 160), (0, 1)], [(247, 220, 255), (1, 1)],
         [(255, 249, 223), (1, 0)], [(255, 117, 110), (0, 0)]],
        [[(255, 168, 154), (0, 1)], [(224, 85, 113), (1, 1)],
         [(255, 243, 100), (1, 0)], [(255, 191, 99), (0, 0)]],
    ]

    colour_list3 = [
        [[(255, 195, 237), (0, 1)], [(227, 245, 255), (1, 1)],
         [(119, 209, 254), (1, 0)], [(92, 111, 125), (0, 0)]],
        [[(103, 109, 126), (0, 1)], [(255, 224, 131), (1, 1)],
         [(169, 185, 218), (1, 0)], [(72, 144, 166), (0, 0)]],
        [[(220, 231, 255), (0, 1)], [(101, 157, 224), (1, 1)],
         [(255, 216, 173), (1, 0)], [(54, 50, 65), (0, 0)]],
        [[(12, 32, 57), (0, 1)], [(86, 145, 214), (1, 1)],
         [(249, 189, 153), (1, 0)], [(230, 242, 255), (0, 0)]],
        [[(28, 34, 67), (0, 1)], [(3, 67, 81), (1, 1)],
         [(236, 236, 255), (1, 0)], [(255, 189, 180), (0, 0)]],
        [[(161, 199, 255), (0, 1)], [(34, 62, 103), (1, 1)],
         [(255, 144, 130), (1, 0)], [(140, 212, 255), (0, 0)]],
        [[(209, 223, 255), (0, 1)], [(70, 99, 180), (1, 1)],
         [(157, 141, 180), (1, 0)], [(255, 174, 147), (0, 0)]],
        [[(255, 200, 199), (0, 1)], [(169, 219, 255), (1, 1)],
         [(72, 83, 120), (1, 0)], [(236, 245, 255), (0, 0)]],
        [[(255, 158, 137), (0, 1)], [(69, 95, 115), (1, 1)],
         [(199, 220, 255), (1, 0)], [(166, 245, 255), (0, 0)]],
    ]

    colour_size = (2, 2)
    # use 4 random colours for now
    # c1, c2, c3, c4 = ((33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69))
    # c1 = (255, 0, 0)
    # c2 = (0, 255, 0)
    # c3 = (0, 0, 255)
    # c4 = (150, 150, 150)

    # constants are blocks that won't move.
    constants = []

    # general block
    constants.append((0, 0))
    constants.append((x_step - 1, y_step - 1))
    constants.append((0, y_step - 1))
    constants.append((x_step - 1, 0))

    # center block
    constants.append((((x_step - 1) / 2), ((y_step - 1) / 2)))

    # 7x7 block
    # constants.append((0, 0))
    # constants.append((6, 6))
    # constants.append((0, 6))
    # constants.append((6, 0))
    # constants.append((3, 3))

    # createColourGridyx(windowSize, c1, c2, c3, c4, x_step, y_step, constants)

    steps = x_step, y_step
    level = testWindow, colours, colour_size, constants, win_size, steps
    run_level(level)
