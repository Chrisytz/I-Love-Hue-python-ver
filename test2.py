""" moveCircle.py
    create a blue circle sprite and have it
    follow the mouse"""

import pygame, random

pygame.init()

screen = pygame.display.set_mode((640, 480))


class Circle(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill((0,0,0))
        self.colour = colour
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.id = id

class overlay(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.set_alpha(128)
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.hover = False
        self.id = id

def main():
    pygame.display.set_caption("move the circle with the mouse")

    background = pygame.Surface(screen.get_size())
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    allSprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    single = pygame.sprite.GroupSingle()

    for i in range (0,3):
        allSprites.add(Circle(colour_list_circle[i], 25+ i*150, 25, i))
    allSprites.draw(screen)

    count = 0
    for sprite in allSprites:
        pygame.draw.ellipse(screen, colour_list_circle[count], sprite.rect)
        count +=1

    for i in range (0,3):
        sprites.add(overlay((0,0,0), 25+ i*150, 25, i))

    for sprite in sprites:
        screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

    pygame.display.update()
    keepGoing = True
    # hide mouse
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in sprites:
                    if sprite.rect.collidepoint(pos):
                        sprite.hover = True
            if event.type == pygame.MOUSEBUTTONUP:
                for sprite in sprites:
                    sprite.hover = False

            for a in sprites:
                if a.hover == True:
                    print(a.colour)
                    a.colour = (255,255,255)
                    a.image.fill(a.colour)
                    print(a.colour)

            for sprite in sprites:
                screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

            # for sprite in single:
            #     screen.fill((0,0,0))
            #     allSprites.draw(screen)
            #     screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
            #     print(sprite.colour)




if __name__ == "__main__":
    main()
