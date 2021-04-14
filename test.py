import pygame
import random

winSize = 400
rectSize = 50 #must be a factor of winSize
numRect = (int)(winSize/rectSize)

### initialisation
pygame.init()
window = pygame.display.set_mode((winSize, winSize))
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

def getColours(winDimensions, rectDimensions):
    x = 0
    list = []
    for j in range(0, winDimensions-1, rectDimensions):
        for i in range(0, winDimensions-1, rectDimensions):
            list.insert(x, pygame.Surface.get_at(window, (j, i)))
            x = x + 1
    return list

class Key(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, colour, id):
        super(Key, self).__init__()
        self.image = pygame.Surface([50,50])
        self.image.fill(colour)
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = ypos
        self.rect.x = xpos

done = False
clock = pygame.time.Clock()

## IT WORKS WOWWWWWWWWW
gradientRect(window, (255, 0, 0), (255, 255, 255), (0, 0, 0), (0, 72, 255), pygame.Rect(0, 0, winSize, winSize))
colourList = getColours(winSize, rectSize)
key_list = pygame.sprite.Group()
num = 0

#drawing the thing
for a in range (0, winSize-1, rectSize):
    for b in range (0, winSize-1, rectSize):
        key_list.add(Key(a,b,colourList[num], len(key_list)+1))
        num = num + 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            if event.button == 1:
                for key in key_list:
                    if key.rect.collidepoint(pos):
                        #another_surface = pygame.Surface((400, 400))
                        #colour = another_surface.get_at((x, y))
                        #pygame.sprite.LayeredUpdates.move_to_front(pygame.sprite.LayeredUpdates.get_sprites_at((key)))
                        window.blit(window, key)
                        key.clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            for key in key_list:
                key.clicked = False

### centering the mouse and rectangle n wtv
    for key in key_list:
        if key.clicked == True:
            pos = pygame.mouse.get_pos()
            key.rect.x = pos[0] - (key.rect.width/2)
            key.rect.y = pos[1] - (key.rect.height/2)

    window.fill((0,0,0))

    key_list.draw(window)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()