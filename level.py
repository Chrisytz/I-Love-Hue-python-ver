# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021

# This describes the function of one level

import sys
import random
import pygame


# Const functions here.

class Grid:
    """
    This class should contain (one) grid which we can use to control everything on each level
    """

    def __init__(self, window, colours, colour_size, constants, window_size, steps):
        self.window = window # window which everything will be drawn onto
        self.colours = colours # colours and their locations.
        self.colour_size = colour_size
        self.constants = constants
        self.window_size = window_size # (x, y) size of window
        self.steps = steps

    def drawGradient(self):
        x_size, y_size = self.window_size
        target_rect = pygame.Rect(0, 0, x_size, y_size)
        colour_rect =pygame.Surface(self.colour_size)
        for i in self.colours:
            pygame.draw.line(colour_rect, i[0], i[1], i[1])
        colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
        self.window.blit(colour_rect, target_rect)
        pygame.display.update()

    def shuffle(self):
        pass


def run_level(level):
    """This will run the entire level!"""
    # Todo: Do we want this to only run one level?
    window, colours, colour_size, constants, window_size, steps = level
    pygame.init() # is pygame already init from another side?
    # window = pygame.display.set_mode((window_size))
    levelgrid = Grid(window, colours, colour_size, constants, window_size, steps)
    levelgrid.drawGradient()

if __name__ == "__main__":
    level = 0 # TODO: CHANGE THIS
    debug = False
    window_size = (400, 400)

    # common sizes for 1200x900
    # 300x300:  x=4     y=3
    # 150x150:  x=8     y=6
    # 100x100:  x=12    y=9
    # 75x75:    x=16    y=12
    # 60x60:    x=20    y=15
    # 50x50:    x=24    y=18

    # for 900x900, 9, 6, 3
    # steps = 8, 8
    steps = 8, 8
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

    colour_size = (2, 2)
    # use 4 random colours for now
    c1, c2, c3, c4 = ((33, 11, 84), (201, 205, 242), (201, 255, 249), (6, 39, 69))
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

    testWindow = pygame.display.set_mode(window_size)
    pygame.display.set_caption("test_window")
    steps = x_step, y_step
    level = testWindow, colours, colour_size, constants, window_size, steps
    run_level(level)
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()