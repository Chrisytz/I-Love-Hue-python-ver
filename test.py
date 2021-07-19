# The original colourgame coded by Christina Zhang, April Break 2021

import sys
import random
import pygame


### initiating variables
size = (1200, 800)


### initialisation
pygame.init()
window = pygame.display.set_mode(size)
pygame.display.set_caption("Gradient Rect")

done = False

def line(window, win_size):
    points = [[(141, 281), (200, 100), (259, 281), (105, 169), (295, 169), (141, 281)],
              [(212, 421), (300, 150), (388, 421), (157, 254), (443, 254), (212, 421)],
              [(282, 562), (400, 200), (518, 562), (210, 338), (590, 338), (282, 562)]]
    thickness = [3,5,7]

    for count in range(5):
        steps_taken = 0
        start_x = int(points[win_size][count][0])
        start_y = int(points[win_size][count][1])
        step_x = (points[win_size][count+1][0]-points[win_size][count][0])/100
        step_y = (points[win_size][count + 1][1] - points[win_size][count][1]) / 100
        while steps_taken < 100:
            #pygame.draw.line(window, (122,122,122), (start_x, start_y), (start_x+step_x, start_y +step_y), 5)
            pygame.draw.circle(window, (255,255,255), (start_x, start_y), thickness[win_size])
            pygame.display.update()
            pygame.time.wait(1)
            start_x += step_x
            start_y += step_y
            steps_taken += 1

    pygame.time.wait(1000)



while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    line(window, 2)
    done = True
        # pygame.draw.rect(window, (122,122,122), (5,5,100,100))
        # pygame.display.update()
        # pygame.time.delay(100)


pygame.quit()
