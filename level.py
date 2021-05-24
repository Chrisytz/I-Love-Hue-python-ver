# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

# This describes the function of one level

import sys
import random
import pygame

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


def getColours(window, window_size, steps):
    x_size, y_size = window_size
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
    def __init__(self, pos, colour, window_size, steps, constant=False):
        pygame.sprite.Sprite.__init__(self)
        rectsize_x = window_size[0] / steps[0]
        rectsize_y = window_size[1] / steps[1]
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

    def __init__(self, window, colours, colour_size, constants, window_size, drawing_size, steps):
        self.window = window  # window which everything will be drawn onto
        self.colours = colours  # colours and their locations.
        self.gradient_size = colour_size
        self.constants = constants
        self.window_size = window_size  # (x, y) size of window
        self.drawing_size = drawing_size
        self.horizontal_limit = (2 / 3) * window_size[0]
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

    def shuffle(self, bypass=False):
        # if you want to bypass grid shuffling
        if bypass:
            return

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
                # self.sprite_list.add(Rect(pos, self.shuffle_grid[i][j], self.window_size, self.steps))



def addColours(colour_list, rect_clicked, circle_clicked):
    colour = []
    for i in range(0, 4):
        colour.append(colour_list[rect_clicked][circle_clicked][i])
    return colour


def evaluate_level(window, levelgrid, sprite_list):
    done = False
    moving_sprite_list = pygame.sprite.GroupSingle()
    # TODO: THIS LIMIT NEEDS TO BE CHANGED TO BE A PASSED VAR TO RESPOND TO SCRREEN SCALING --> levelgrid.horizontalLimit **DONE I THINK**
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                posx, posy = pos
                if DEBUG: print("this is mousebutton down posx, posy: ", pos)
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(pos) and sprite.movable:
                        if DEBUG: print(sprite.constant)
                        sprite.clicked = True
                        moving_sprite_list.add(sprite)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if DEBUG: print("this is mousebutton up pos:", pos)
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(pos) and sprite.movable:
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
                moving_sprite_list.empty()
            if event.type == pygame.MOUSEMOTION:
                posx, posy = pygame.mouse.get_pos()
                for sprite in moving_sprite_list:
                    # iirc the below code should run ok
                    if sprite.clicked == True and sprite.movable and (posx < levelgrid.horizontal_limit):
                        sprite.rect.move_ip(event.rel)
                        moving_sprite_list.draw(window)
            sprite_list.draw(window) #THIS IS WHAT IS DRAWING THE SPRITES!
            moving_sprite_list.draw(window)  # draw this last ALWAYS
            # TODO: FIND A BETTER WAY TO DRAW RECTANGLES
            # in particular, we need a better way to calculate the '200' present here.
            pygame.draw.rect(window, (0, 0, 0),
                             pygame.Rect(levelgrid.horizontal_limit, 0, levelgrid.horizontal_limit / 2,
                                         levelgrid.horizontal_limit))



        pygame.draw.rect(window,(255,255,255), (400, 200, 50,50)) #THIS IS JUST A TEST THING :)
        pygame.display.flip()

        if levelgrid.original_grid == getColours(window, (levelgrid.horizontal_limit, levelgrid.horizontal_limit),
                                                 levelgrid.steps):
            if DEBUG: print("you won")
            done = True #important: we should need this but why dont we wghat
            return 0  # 0 = won the game

            # you've won the game


def run_level(level):
    """This will run the entire level!"""
    isComplete = 1
    # Todo: Do we want this to only run one level?
    # system level variables.
    sprite_list = pygame.sprite.Group()
    sprite_single = pygame.sprite.GroupSingle()

    window, colours, colour_size, constants, window_size, steps = level
    pygame.display.set_caption("LEVEL!!!!!")
    if window_size[0] < window_size[1]:
        drawing_size = (window_size[0], window_size[0])
    else:
        drawing_size = (window_size[1], window_size[1])

    # TODO: horizontal lim to be coded here with diff between drawing size and window sizes

    # pygame.init()  # is pygame already init from another side?
    # window = pygame.display.set_mode((window_size))
    levelgrid = Grid(window, colours, colour_size, constants, window_size, drawing_size, steps)
    if DEBUG: print(constants)
    levelgrid.drawGradient()
    # drawGridLoose(window, window_size, steps, levelgrid.shuffle_grid) # todo: remove
    levelgrid.getColours()
    levelgrid.shuffle()

    levelgrid.addToSpriteGroup(sprite_list)

    if evaluate_level(window, levelgrid, sprite_list) == 0:
        print("you have won")
        iscomplete = 0
    else:
        iscomplete = 1


    return iscomplete

    # sys.exit()

    # at this point, everything has been created properly, hand over to run_game.


def runGame(rect_id, circle_id):
    level = 0  # TODO: CHANGE THIS
    level_complete = 0
    window_size = (600, 400)
    testWindow = pygame.display.set_mode((window_size))

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
        # colourlist1
        [[[(51, 111, 84), (0, 1)], [(180, 239, 255), (1, 1)],
          [(90, 223, 92), (1, 0)], [(91, 112, 82), (0, 0)]],
         [[(84, 107, 78), (0, 1)], [(121, 154, 227), (1, 1)],
          [(40, 128, 104), (1, 0)], [(159, 237, 105), (0, 0)]],
         [[(161, 199, 255), (0, 1)], [(22, 61, 103), (1, 1)],
          [(41, 129, 105), (1, 0)], [(157, 237, 104), (0, 0)]],
         [[(160, 127, 227), (0, 1)], [(226, 245, 255), (1, 1)],
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
          [(170, 255, 213), (1, 0)], [(50, 174, 213), (0, 0)]]],
        # colourlist2
        [[[(211, 90, 63), (0, 1)], [(148, 41, 110), (1, 1)],
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
          [(255, 243, 100), (1, 0)], [(255, 191, 99), (0, 0)]]],
        # colourlist3
        [[[(255, 195, 237), (0, 1)], [(227, 245, 255), (1, 1)],
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
          [(199, 220, 255), (1, 0)], [(166, 245, 255), (0, 0)]]]
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

    if (circle_id == 0 or circle_id == 3 or circle_id == 6):
        x_step = 4
        y_step = 4
    elif (circle_id == 1 or circle_id == 4 or circle_id == 7):
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

    level = testWindow, colours, colour_size, constants, window_size, steps
    run_level(level)
    if (run_level(level) == 0):
        level_complete = 1
    return level_complete


if __name__ == "__main__":
    level = 0  # TODO: CHANGE THIS
    window_size = (400, 400)
    testWindow = pygame.display.set_mode((window_size))
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
    # colours.append([(33, 11, 84), (0, 0)])
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
    level = testWindow, colours, colour_size, constants, window_size, steps
    run_level(level)
