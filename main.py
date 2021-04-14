import sys
import random
import pygame

### Setting up dimensions
winSize = 400
rectSize = 50 #must be a factor of winSize
numRect = (int)(winSize/rectSize)

### initialisation
pygame.init()
window = pygame.display.set_mode((winSize, winSize))
pygame.display.set_caption("Gradient Rect")

### functions
# TODO: maybe fix the bottomleft things bc theyre wrong xd
def gradientRect(window, topleft_colour, topright_colour, bottomright_colour, bottomleft_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2,2 ))                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, bottomleft_colour, (0,0), (0,0))         # left colour line
    pygame.draw.line( colour_rect, topright_colour, (1,1), (1,1))
    pygame.draw.line( colour_rect, bottomright_colour, (1,0), (1,0))
    pygame.draw.line( colour_rect, topleft_colour, (0,1), (0,1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height ))  # stretch!
    window.blit(colour_rect, target_rect)                                    # paint it

def getColours(winDimensions, rectDimensions):
    x = 0
    list = []
    for j in range(0, winDimensions-1, rectDimensions):
        for i in range(0, winDimensions-1, rectDimensions):
            list.insert(x, pygame.Surface.get_at(window, (j, i)))
            x = x + 1
    return list

def shuffle(list, numRect):
    shuffledList = list[1:numRect-1] + list [numRect:-numRect] + list[-(numRect-1):-1]
    random.shuffle(shuffledList)
    return shuffledList

def replace(shuffledList, list, numRect) :
    list[1:numRect-1] = shuffledList[0:numRect-2]
    list[numRect:-numRect] = shuffledList[numRect-2:-(numRect-2)]
    list[-(numRect-1):-1] = shuffledList[-(numRect-2):]
    return list

def draw(list, winDimensions, rectDimensions):
    x = 0
    for j in range (0, winDimensions-1, rectDimensions):
        for i in range (0, winDimensions-1, rectDimensions):
            pygame.draw.rect(window, list[x], (j, i, rectDimensions, rectDimensions))
            x=x+1

### creating gradiented rectangles
gradientRect(window, (255, 0, 0), (255, 255, 255), (0, 0, 0), (0, 72, 255), pygame.Rect(0, 0, winSize, winSize))

colourList = getColours(winSize, rectSize)
draw(colourList, winSize, rectSize)
pygame.display.update()
pygame.time.delay(1000)

#print(colourList)
#print(shuffle(colourList, numRect))
#print(replace(shuffle(colourList, numRect), colourList, numRect))

shuffledColourList = replace(shuffle(colourList, numRect), colourList, numRect)
draw(shuffledColourList, winSize, rectSize)

pygame.display.update()

### Main Loop
game_over = False
while not game_over:

    # Handle user-input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()