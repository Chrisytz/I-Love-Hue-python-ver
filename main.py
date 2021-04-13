import sys
import random
import pygame

# TODO: recognize that anni is a superior being and will not be stopped

# Window size
WINDOW_WIDTH    = 400
WINDOW_HEIGHT   = 400

### initialisation
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gradient Rect")

def gradientRect(window, topleft_colour, topright_colour, bottomright_colour, bottomleft_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2,2 ))                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, bottomleft_colour, (0,0), (0,0))         # left colour line
    pygame.draw.line( colour_rect, topright_colour, (1,1), (1,1))
    pygame.draw.line( colour_rect, bottomright_colour, (1,0), (1,0))
    pygame.draw.line( colour_rect, topleft_colour, (0,1), (0,1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height ))  # stretch!
    window.blit(colour_rect, target_rect)                                    # paint it

def getColours():
    x = 0
    list = []
    for j in range(0, 399, 50):
        for i in range(0, 399, 50):
            list.insert(x, pygame.Surface.get_at(window, (j, i)))
            x = x + 1
    return list

def shuffle(list):
    random.shuffle(list)
    shuffled = list
    return list

def draw(xd):
    x = 0
    for j in range (0, 399, 50):
        for i in range (0, 399, 50):
            pygame.draw.rect(window, xd[x], (j, i, 50, 50))
            x=x+1

gradientRect(window, (255, 0, 0), (255, 255, 255), (0, 0, 0), (0, 72, 255), pygame.Rect(0, 0, 400, 400))

boop = getColours()
draw(boop)
print(boop)
pygame.display.update()
shuffled = shuffle(getColours())
draw(shuffled)

pygame.draw.rect(window, boop[0], (0,0,50,50))
pygame.draw.rect(window, boop[7], (0,350,50,50))
pygame.draw.rect(window, boop[63], (350, 350, 50, 50))
pygame.draw.rect(window, boop[-8], (350, 0, 50, 50))

pygame.display.update()

### Main Loop
game_over = False
while not game_over:

    # Handle user-input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()