# The original colourgame coded by Christina Zhang, April Break 2021

import sys
import random
import pygame

import config

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

array = [["Circles2/0.png", "Circles2/1.png"]]
array2 = []
circle1 = pygame.image.load(array[0][0])
circle1 = pygame.transform.smoothscale(circle1, (100,100))

count = 0
for circle in array:
    array2.append(pygame.image.load(array[0][count]))
    count += 1

window.blit(array2[0], (0,0))

pygame.display.update()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


pygame.quit()
