# Currently draws circle overlay with on-click brighten.


import pygame, random

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


class Overlay(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.set_alpha(128)
        self._original_colour = colour
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.hover = False
        self.id = id

    def getOriginalColour(self):
        return self._original_colour

def drawCircles():
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption("circles")

    background = pygame.Surface(screen.get_size())
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    circle_sprites = pygame.sprite.Group()
    overlay_sprites  = pygame.sprite.Group()
    single = pygame.sprite.GroupSingle()

    for i in range(0, 3):
        circle_sprites.add(Circle(colour_list_circle[i], 25 + i * 150, 25, i))
    circle_sprites.draw(screen)

    count = 0
    for sprite in circle_sprites:
        pygame.draw.ellipse(screen, colour_list_circle[count], sprite.rect)
        count += 1
    for i in range(0, 3):
        overlay_sprites.add(Overlay((0, 0, 0), 25 + i * 150, 25, i))

    for sprite in overlay_sprites:
        screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

    pygame.display.update()
    # hide mouse
    done = False
    while not done:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for overlay_sprite in overlay_sprites:
                    if overlay_sprite.rect.collidepoint(mouse_pos):
                        overlay_sprite.hover = True
            if event.type == pygame.MOUSEBUTTONUP:
                for overlay_sprite in overlay_sprites:
                    overlay_sprite.hover = False
                    overlay_sprite.colour = overlay_sprite.getOriginalColour()
                    overlay_sprite.hover = False

            for mysprite in overlay_sprites:
                if mysprite.hover:
                    mysprite.colour = (255, 255, 255)
                    mysprite.image.fill(mysprite.colour)
                    overlay_sprites.draw(screen)


if __name__=="__main__":
    drawCircles()