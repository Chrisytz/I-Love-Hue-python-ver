# Colour Game 2021 Christina Zhang & Anthony Luo
# ♪(ϞϞ(๑⚈ ․̫ ⚈๑)∩
# April 2021


import sys
import random
import pygame

win_width = 600
win_height = 400
done = False
pygame.init()
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Gradient Rect")

# HAVE MULTIPLE SURFACES AND JUST SCROLL ONE
# LINK: https://www.pygame.org/docs/ref/mouse.html --> pygame.MOUSEWHEEL
test_colour_list = [[(0,0,255), (0,255,0), (255,0,255), (255,255,0)],[(255,0,255), (0,255,0), (0,0,255), (255,255,0)],[(0,255,255), (0,255,0), (255,0,255), (255,255,0)]]
for i in range (0, 3):
    for j in range (0,4):
        pygame.draw.rect(window, test_colour_list[i][j], (20+ (40*j), (20*(i+1)) + (40*i), 40, 40))


pygame.display.update()
# This is the main entry point to the game.
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()

# create loading screen!

# create level selection screen !

# create configuration screen !


if __name__ == "__main__":
    print("This is the main file!")