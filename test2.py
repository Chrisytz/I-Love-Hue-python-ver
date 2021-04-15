import sys
import random
import pygame
import math

### initiating variables
win_size = 400
rect_size = 200 #must be a factor of win_size
num_rect = (int)(win_size/rect_size)
done = False
sprite_list = pygame.sprite.Group()
sprite_list2 = pygame.sprite.GroupSingle(sprite=None)
location_x = 0
location_y = 0
x = 0
y = 0
sprite_swap1 = pygame.sprite.GroupSingle(sprite = None)
sprite_swap2 = pygame.sprite.GroupSingle(sprite = None)
spril_list_collide = pygame.sprite.GroupSingle(sprite = None)

### initialisation
pygame.init()
window = pygame.display.set_mode((win_size, win_size))
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

def getColours(win_dimensions, rect_dimensions):
    count = 0
    list = []
    for i in range(0, win_dimensions-1, rect_dimensions):
        for j in range(0, win_dimensions-1, rect_dimensions):
            list.insert(count, pygame.Surface.get_at(window, (i, j)))
            count += 1
    return list

def shuffle(list, num_rect):
    shuffled_list = list[1:num_rect-1] + list[num_rect:-num_rect] + list[-(num_rect-1):-1]
    random.shuffle(shuffled_list)
    return shuffled_list

def replace(shuffled_list, list, num_rect) :
    list[1:num_rect-1] = shuffled_list[0:num_rect-2]
    list[num_rect:-num_rect] = shuffled_list[num_rect-2:-(num_rect-2)]
    list[-(num_rect-1):-1] = shuffled_list[-(num_rect-2):]
    return list

def draw(list, win_dimensions, rect_dimensions):
    count = 0
    for i in range (0, win_dimensions-1, rect_dimensions):
        for j in range (0, win_dimensions-1, rect_dimensions):
            pygame.draw.rect(window, list[count], (i, j, rect_dimensions, rect_dimensions))
            count += 1

def spriteGroup(shuffled_colour_list, win_size, rect_size, sprite_list):
    count = 0
    for i in range(0, win_size - 1, rect_size):
        for j in range(0, win_size - 1, rect_size):
            sprite_list.add(RectSprite(i, j, shuffled_colour_list[count], len(sprite_list) + 1))
            count += 1
    return sprite_list

### creating gradiented rectangles
gradientRect(window, (255, 0, 0), (255, 255, 255), (0, 0, 0), (0, 72, 255), pygame.Rect(0, 0, win_size, win_size))
colour_list = getColours(win_size, rect_size)
draw(colour_list, win_size, rect_size)
shuffled_colour_list = replace(shuffle(colour_list, num_rect), colour_list, num_rect)
pygame.display.update()
pygame.time.delay(1000)


class RectSprite(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, colour, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([rect_size, rect_size])
        self.colour = colour
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = y_pos
        self.rect.x = x_pos
#asdadadadasdadsfasfdasf
    def getColour(self):
        return self.colour

# drawing the thing
spriteGroup(shuffled_colour_list, win_size, rect_size, sprite_list)

while not done:
    sprite_list.draw(window)

    # pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0] # x pos of mouse on press
            y = pos[1] # y pos of mouse on press
            print(x)
            print(y)
            if event.button == 1:
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(pos):
                        sprite.clicked = True
                        sprite_list2.add(sprite)
        if event.type == pygame.MOUSEBUTTONUP:
            location = pygame.mouse.get_pos()
            location_x = location[0]  # x pos of mouse on release
            location_y = location[1]  # y pos of mouse on release
            for sprite in sprite_list:
                sprite.clicked = False
                print(location_x)
                print(location_y)

    for sprite in sprite_list2:
        if sprite.clicked == True:
            pos = pygame.mouse.get_pos()
            sprite.rect.x = pos[0] - sprite.rect.width / 2
            sprite.rect.y = pos[1] - sprite.rect.height / 2
        sprite_list2.draw(window)
        if sprite.clicked == False:

            sprite_list_collide = pygame.sprite.spritecollide(sprite, sprite_list, False)
            sprite_swap1.add(RectSprite(math.floor(location_x/rect_size)*rect_size, math.floor(location_y/rect_size)*rect_size, sprite.colour, len(sprite_swap1)+1))
            for sprite2 in sprite_list_collide:
                sprite_swap2.add(RectSprite(math.floor(x/rect_size)*rect_size, math.floor(y/rect_size)*rect_size, sprite2.colour, len(sprite_swap2)+1))
            # for spriteA in sprite_swap2:
            #     sprite_list.add(spriteA)
            # for spriteB in sprite_swap1:
            #     sprite_list.add(spriteB)
        sprite_swap2.draw(window)
        sprite_swap1.draw(window)

    pygame.display.flip()

pygame.quit()