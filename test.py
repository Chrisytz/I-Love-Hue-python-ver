# The original colourgame coded by Christina Zhang, April Break 2021

import sys
import random
import pygame

### initiating variables
size = 600, 400
win_size = 800
rect_size = 200  # must be a factor of win_size
num_rect = (int)(win_size / rect_size)
done = False
sprite_list = pygame.sprite.Group()
sprite_list2 = pygame.sprite.GroupSingle(sprite=None)


### initialisation
pygame.init()
window = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption("Gradient Rect")

class Circle(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, win_vars, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((win_vars["circle_size"], win_vars["circle_size"]))
        self.image.fill((0, 0, 0))
        self.colour = colour
        self._original_colour = colour
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.id = id

    def getOriginalColour(self):
        return self._original_colour

    def drawCircle(self, screen):
        pygame.draw.ellipes(screen, self.colour, self.rect)

colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
circle_sprite_list = pygame.sprite.Group()

win_vars = {
    "bar_thickness": size[1] * 0.05,
    "sprite_size": ((size[0] / 3) - (size[1] * 0.1)) / 4,
    "width_sidebar": size[0] / 3,
    "bottom_bar_loc": size[1] * 0.95,
    "black": (0, 0, 0),
    "num_of_rectangles": 3,
    "circle_size": ((size[0] * (2 / 3)) - (4 * size[1] * 0.05)) / 3,
    "space_between_circles": size[1] * 0.05
}


### functions
def gradientRect(window, topleft_colour, topright_colour, bottomright_colour, bottomleft_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, topleft_colour, (0, 0), (0, 0))
    pygame.draw.line(colour_rect, bottomright_colour, (1, 1), (1, 1))
    pygame.draw.line(colour_rect, topright_colour, (1, 0), (1, 0))
    pygame.draw.line(colour_rect, bottomleft_colour, (0, 1), (0, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (300, 300))  # stretch!
    window.blit(colour_rect, target_rect)# paint it

def addCircleSprites(colour_list_circle, circle_sprites, win_vars):
    for i in range(0, 3):
        for j in range(0, 3):
            circle_sprites.add(Circle(colour_list_circle[i],
                                      (win_vars["width_sidebar"] + win_vars["bar_thickness"]) + i * (
                                              win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars["bar_thickness"] + j * (
                                              win_vars["circle_size"] + win_vars["space_between_circles"]),
                                      win_vars, i))
    return circle_sprites

def drawCircles(window, colour_list_circle, circle_sprites):
    for sprite in circle_sprites:
        pygame.draw.ellipse(window, colour_list_circle[0], sprite.rect)
### creating gradiented rectangles

gradientRect(window, (245, 255, 250), (255, 247, 235), (181, 27, 58), (17, 51, 173),
             pygame.Rect(0, 0, win_size, win_size))

circle_sprite_list = addCircleSprites(colour_list_circle, circle_sprite_list, win_vars)

circle_sprite_list.draw(window)

surface = drawCircles(window, colour_list_circle, circle_sprite_list)


gradientRect(window, (245, 255, 250), (255, 247, 235), (181, 27, 58), (17, 51, 173), surface)


pygame.display.update()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
