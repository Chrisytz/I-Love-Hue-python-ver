# Currently draws circle overlay with on-click brighten.


import pygame, random, sys


class Circle(pygame.sprite.Sprite):
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
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


class Overlay(pygame.sprite.Sprite):
    # overlay is a really bad name but that's ok we will go with it
    def __init__(self, colour, x_pos, y_pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.alpha = 128
        self.image.set_alpha(128)
        self._original_colour = colour
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.hover = False
        self.clicked = False
        self.id = id

    def getOriginalColour(self):
        return self._original_colour

    def fillImage(self, alpha):
        self.image.set_alpha(alpha)
        self.image.fill(self.colour)


def drawCircles():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("circles")

    background = pygame.Surface(screen.get_size())
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    circle_sprites = pygame.sprite.Group()
    overlay_sprites = pygame.sprite.Group()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for overlay_sprite in overlay_sprites:
                    if overlay_sprite.rect.collidepoint(mouse_pos):
                        overlay_sprite.clicked = True
                for circle_sprite in circle_sprites:
                    if circle_sprite.rect.collidepoint(mouse_pos):
                        circle_sprite.clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                for overlay_sprite in overlay_sprites:
                    overlay_sprite.clicked = False
                    overlay_sprite.colour = overlay_sprite.getOriginalColour()
                    overlay_sprite.image.fill(overlay_sprite.colour)
                for circle_sprite in circle_sprites:
                    circle_sprite.clicked = False

            for mysprite in overlay_sprites:
                if mysprite.clicked:
                    mysprite.colour = (255, 255, 255)
                    mysprite.image.fill(mysprite.colour)

        # circle_sprites.draw(screen)
        count = 0
        for sprite in circle_sprites:
            pygame.draw.ellipse(screen, colour_list_circle[count], sprite.rect)
            count += 1
        for sprite in overlay_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        # overlay_sprites.draw(screen)

        pygame.display.update()


def drawCircles2():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("circles")

    background = pygame.Surface(screen.get_size())
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    circle_sprites = pygame.sprite.Group()
    overlay_sprites = pygame.sprite.Group()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for overlay_sprite in overlay_sprites:
                    if overlay_sprite.rect.collidepoint(mouse_pos):
                        overlay_sprite.clicked = True
                for circle_sprite in circle_sprites:
                    if circle_sprite.rect.collidepoint(mouse_pos):
                        circle_sprite.clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                for overlay_sprite in overlay_sprites:
                    overlay_sprite.clicked = False
                    overlay_sprite.colour = overlay_sprite.getOriginalColour()
                    overlay_sprite.image.fill(overlay_sprite.colour)
                for circle_sprite in circle_sprites:
                    circle_sprite.clicked = False

            for mysprite in overlay_sprites:
                if mysprite.clicked:
                    mysprite.colour = (255, 255, 255)
                    # pygame.draw.ellipse(screen, mysprite.colour, mysprite.rect)
                    mysprite.image.fill(mysprite.colour)

        circle_sprites.draw(screen)
        count = 0
        for sprite in circle_sprites:
            pygame.draw.ellipse(screen, colour_list_circle[count], sprite.rect)
            count += 1
        for sprite in overlay_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        # overlay_sprites.draw(screen)

        pygame.display.update()


def drawCircles3():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("circles")

    background = pygame.Surface(screen.get_size())
    colour_list_circle = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]
    circle_sprites = pygame.sprite.Group()
    overlay_sprites = pygame.sprite.Group()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in overlay_sprites:
                    if sprite.rect.collidepoint(mouse_pos):
                        sprite.clicked = True
                        sprite.alpha = 0
                        sprite.fillImage(0)
            if event.type == pygame.MOUSEBUTTONUP:
                for sprite in overlay_sprites:
                    sprite.clicked = False
                    sprite.alpha = 128
                    sprite.fillImage(128)

            # circle_sprites.draw(screen)
            count = 0
            for sprite in circle_sprites:
                pygame.draw.ellipse(screen, sprite.colour, sprite.rect)
                count += 1

            for sprite in overlay_sprites:
                screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

        pygame.display.update()



def drawGradientCircles():
    pygame.init()
    colours = []
    colours.append([(255, 255, 255), (0, 0)])
    colours.append([(168, 220, 255), (0, 1)])
    colours.append([(0, 29, 69), (1, 1)])
    colours.append([(255, 171, 107), (1, 0)])
    colour_size = (2, 2)

    window = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("anni is crying")

    target_rect = pygame.Rect(0,0, 400, 400)
    colour_rect = pygame.Surface((2,2))
    for i in colours:
        pygame.draw.line(colour_rect, i[0], i[1], i[1])
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)

if __name__ == "__main__":
    drawGradientCircles()
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()