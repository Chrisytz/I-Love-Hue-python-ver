# The original colourgame coded by Christina Zhang, April Break 2021

import sys
import random
import pygame

### initiating variables
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


### functions
def gradientRect(window, topleft_colour, topright_colour, bottomright_colour, bottomleft_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, topleft_colour, (0, 0), (0, 0))
    pygame.draw.line(colour_rect, bottomright_colour, (1, 1), (1, 1))
    pygame.draw.line(colour_rect, topright_colour, (1, 0), (1, 0))
    pygame.draw.line(colour_rect, bottomleft_colour, (0, 1), (0, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)  # paint it


def getColours(win_dimensions, rect_dimensions):
    count = 0
    list = []
    for i in range(0, win_dimensions - 1, rect_dimensions):
        for j in range(0, win_dimensions - 1, rect_dimensions):
            list.insert(count, pygame.Surface.get_at(window, (i, j)))
            count += 1
    return list


def shuffle(list, num_rect):
    shuffled_list = list[1:num_rect - 1] + list[num_rect:-num_rect] + list[-(num_rect - 1):-1]
    random.shuffle(shuffled_list)
    return shuffled_list


def replace(shuffled_list, list, num_rect):
    list[1:num_rect - 1] = shuffled_list[0:num_rect - 2]
    list[num_rect:-num_rect] = shuffled_list[num_rect - 2:-(num_rect - 2)]
    list[-(num_rect - 1):-1] = shuffled_list[-(num_rect - 2):]
    return list


def draw(list, win_dimensions, rect_dimensions):
    count = 0
    for i in range(0, win_dimensions - 1, rect_dimensions):
        for j in range(0, win_dimensions - 1, rect_dimensions):
            pygame.draw.rect(window, list[count], (i, j, rect_dimensions, rect_dimensions))
            pygame.display.update()
            pygame.time.delay(15)
            count += 1


def spriteGroup(shuffled_colour_list, win_size, rect_size, sprite_list):
    count = 0
    for i in range(0, win_size - 1, rect_size):
        for j in range(0, win_size - 1, rect_size):
            sprite_list.add(RectSprite(i, j, shuffled_colour_list[count], len(sprite_list) + 1))
            count += 1
    return sprite_list


def paintWhite(win_size, rect_size):
    count = 0
    for i in range(0, win_size - 1, rect_size):
        for j in range(0, win_size - 1, rect_size):
            pygame.draw.rect(window, (190, 232, 237), (i, j, rect_size, rect_size))
            pygame.display.update()
            pygame.time.delay(20)
            count += 1


### creating gradiented rectangles
gradientRect(window, (245, 255, 250), (255, 247, 235), (181, 27, 58), (17, 51, 173),
             pygame.Rect(0, 0, win_size, win_size))
colour_list = getColours(win_size, rect_size)
colour_list_to_compare = getColours(win_size, rect_size)
pygame.draw.rect(window, (0, 0, 0), (0, 0, win_size, win_size))
draw(colour_list, win_size, rect_size) # not actually very important.
shuffled_colour_list = replace(shuffle(colour_list, num_rect), colour_list, num_rect)
pygame.display.update()
pygame.time.delay(1000)


class RectSprite(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, colour, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([rect_size, rect_size])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = y_pos
        self.rect.x = x_pos
        self.original_x = x_pos
        self.original_y = y_pos
        self.colour = colour


# drawing the thing
spriteGroup(shuffled_colour_list, win_size, rect_size, sprite_list)

while not done:

    sprite_list.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            position_x = position[0]  # x pos of mouse on press
            position_y = position[1]  # y pos of mouse on press
            print(position_x, position_y)
            if event.button == 1:
                for sprite in sprite_list:
                    colour = sprite.colour
                    if sprite.rect.collidepoint(position):
                        print(colour)
                        if colour != shuffled_colour_list[0] and colour != shuffled_colour_list[
                            num_rect - 1] and colour != shuffled_colour_list[-num_rect] and colour != \
                                shuffled_colour_list[-1]:
                            sprite.clicked = True
                            sprite_list2.add(sprite)
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            position_x = position[0]  # x pos of mouse on release
            position_y = position[1]  # y pos of mouse on release
            for sprite in sprite_list:
                if sprite.rect.collidepoint(position):
                    for sprite2 in sprite_list2:
                        colour = sprite2.colour
                        if colour != shuffled_colour_list[0] and colour != shuffled_colour_list[
                            num_rect - 1] and colour != shuffled_colour_list[-num_rect] and colour != \
                                shuffled_colour_list[-1]:
                            sprite.rect.x = sprite2.original_x
                            sprite.rect.y = sprite2.original_y
                            sprite2.rect.x = sprite.original_x
                            sprite2.rect.y = sprite.original_y
                            sprite.original_x = sprite.rect.x
                            sprite.original_y = sprite.rect.y
                            sprite2.original_x = sprite2.rect.x
                            sprite2.original_y = sprite2.rect.y
                sprite.clicked = False
            sprite_list2.empty()

    for sprite in sprite_list2:
        if sprite.clicked == True:
            pos = pygame.mouse.get_pos()
            sprite.rect.x = pos[0] - sprite.rect.width / 2
            sprite.rect.y = pos[1] - sprite.rect.height / 2
            # print(sprite.rect.x, sprite.rect.y)
            # print(pos[0], pos[1])
        sprite_list2.draw(window)

    pygame.display.flip()

    colour_compare = getColours(win_size, rect_size)
    if colour_compare == colour_list_to_compare:
        pygame.time.delay(1000)
        # paintWhite(win_size, rect_size)
        img = pygame.image.load("animewin.png").convert_alpha()
        img2 = pygame.transform.smoothscale(img, (win_size, win_size))
        window.blit(img2, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        done = True

pygame.quit()
