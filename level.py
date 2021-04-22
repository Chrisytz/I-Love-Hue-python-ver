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

    def __init__(self, colours, constants, window_size, blocks):
        self.colours = colours
        self.constants = constants
        self.window_size = window_size
        self.blocks = blocks



def run_level():
    """This will run the entire level!"""
    pygame.init() # is pygame already init from another side?