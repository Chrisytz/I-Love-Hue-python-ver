import pygame
import sys
import random
from sound import Sound
import config

#todo: im gonna create a fucking text class because i am losing my fucking mind rn o m g w t f i s wrong with THISSSSKHADFKHASFD
class Settings(pygame.sprite.Sprite):
    def __init__(self, colour, win_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((win_size[0], win_size[1]))
        self.colour = colour
        self.image.set_alpha(0)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.open = False

    def fillWindow(self, alpha):
        self.image.set_alpha(alpha)
        self.image.fill(self.colour)

    def updateColour(self, colour):
        self.image.fill(colour)
        self.rect = self.image.get_rect()

class Buttons(pygame.sprite.Sprite):
    def __init__(self, text, textColour, textClickedColour, backgroundColour, font, x_pos, y_pos, clickable):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.textColour = textColour
        self.textClickedColour = textClickedColour
        self.backgroundColour = backgroundColour
        self.image = font.render(self.text, True, self.textColour, self.backgroundColour)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.clicked = False
        self.clickable = clickable
        self.hover = False

    def onClick(self, font):
        # self.textColour = textColour
        if self.clickable == True:
            self.image = font.render(self.text, True, self.textClickedColour, self.backgroundColour)
            self.rect = self.image.get_rect()
            self.rect.x = self.x_pos
            self.rect.y = self.y_pos

    def changeMode(self, font, backgroundColour, textColour, textClickedColour):
        self.textColour = textColour
        self.textClickedColour = textClickedColour
        self.backgroundColour = backgroundColour
        self.image = font.render(self.text, True, self.textColour, self.backgroundColour)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def reset(self, font):
        self.image = font.render(self.text, True, self.textColour, self.backgroundColour)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

def createButtons(backgroundColour, lmt, lmtc, dmt, dmtc, win_vars):

    font = pygame.font.Font('Quicksand-Regular.ttf', int(win_vars["font_size"]))

    if backgroundColour == (255, 244, 234):
        textColour = lmt
        textClickedColour = lmtc
    else:
        textColour = dmt
        textClickedColour = dmtc

    light_mode = Buttons("LIGHT MODE", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"], win_vars["sprite_size"] * 1.2, True)
    dark_mode = Buttons("DARK MODE", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"], light_mode.rect.bottomright[1] + win_vars["sprite_size"], True)

    cursor = Buttons("CURSOR:", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"], dark_mode.rect.bottomright[1] + win_vars["sprite_size"], False)
    cursor_circle = Buttons("CIRCLE", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"]/1.5 + cursor.rect.topright[0], dark_mode.rect.bottomright[1] + win_vars["sprite_size"], True)
    cursor_cross = Buttons("CROSS", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"]/1.5 + cursor_circle.rect.topright[0], dark_mode.rect.bottomright[1] + win_vars["sprite_size"], True)
    cursor_arrow = Buttons("ARROW", textColour, textClickedColour, backgroundColour, font,win_vars["sprite_size"]/1.5 + cursor_cross.rect.topright[0], dark_mode.rect.bottomright[1] + win_vars["sprite_size"], True)

    window_size = Buttons("WINDOW SIZE:", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"], cursor.rect.bottomright[1] + win_vars["sprite_size"], False)
    small = Buttons("600 x 400", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"] / 1.5 + window_size.rect.topright[0], cursor.rect.bottomright[1] + win_vars["sprite_size"], True)
    medium = Buttons("900 x 600", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"] / 1.5 + small.rect.topright[0], cursor.rect.bottomright[1] + win_vars["sprite_size"], True)
    large = Buttons("1200 x 800", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"] / 1.5 + medium.rect.topright[0], cursor.rect.bottomright[1] + win_vars["sprite_size"], True)

    sound = Buttons("SOUND:", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"], window_size.rect.bottomright[1] + win_vars["sprite_size"], False)
    sound_on = Buttons("ON", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"] / 1.5 + sound.rect.topright[0], window_size.rect.bottomright[1] + win_vars["sprite_size"], True)
    sound_off = Buttons("OFF", textColour, textClickedColour, backgroundColour, font, win_vars["sprite_size"] / 1.5 + sound_on.rect.topright[0], window_size.rect.bottomright[1] + win_vars["sprite_size"], True)

    button_list = [light_mode, dark_mode, cursor, cursor_circle, cursor_cross, cursor_arrow, window_size, small, medium, large, sound, sound_on, sound_off]

    return button_list

def changeColour(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue
    return surface

def settings(win_vars, current_cursor, textHoverColour, textColour, settingColour,
          sidebarColour, window, event, adj, winsize, settingsPage, circles_visible, rect_can_be_clicked, cursor_list, lmt, lmtc, dmt, dmtc, data):
    pygame.init()
    win_size = winsize
    window = pygame.display.set_mode((win_size))
    pygame.display.set_caption("SETTINGGSSSADAD")

    done = False

    font = pygame.font.Font('Quicksand-Regular.ttf', int(win_vars["font_size"]))
    # button_list = [lightMode, darkMode, circle, x, arrow]
    cursor_value = current_cursor
    backgroundColour = settingColour
    sideColour = sidebarColour
    backgroundValue = None
    winDim = win_size
    windim_pressed = False
    button_list = createButtons(backgroundColour, lmt, lmtc, dmt, dmtc, win_vars)



    close_button = changeColour(pygame.transform.smoothscale(pygame.image.load('x.png').convert_alpha(), (int(win_vars["sprite_size"] / 2), int(win_vars["sprite_size"] / 2))),
                                textColour[0], textColour[1], textColour[2])

    close_rect = close_button.get_rect(topleft = (win_vars["sprite_size"]/4, win_vars["sprite_size"]/4))

    while not done:
        # settingsPage.update
        window.blit(settingsPage.image, (0, 0, win_size[0], win_size[1]))

        if settingsPage.colour == (255, 244, 234):
            textColour = lmt
            textClickedColour = lmtc
        else:
            textColour = dmt
            textClickedColour = dmtc

        for button in button_list:
            window.blit(button.image, button.rect)

        for button in button_list:
            if button.hover == True:
                button.onClick(font)
            else:
                button.reset(font)
        window.blit(close_button, close_rect)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            for button in button_list:
                if button.rect.collidepoint(pos) and button.clickable:
                    button.hover = True
                else:
                    button.hover = False

            if close_rect.collidepoint(pos):
                close_button = changeColour(close_button, textClickedColour[0], textClickedColour[1], textClickedColour[2])
            else:
                close_button = changeColour(close_button, textColour[0], textColour[1], textColour[2])


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if button_list[0].rect.collidepoint(pos):
                    close_button = changeColour(close_button, textColour[0], textColour[1], textColour[2])
                    settingsPage.colour = (255, 244, 234)
                    settingsPage.updateColour((255, 244, 234))
                    backgroundColour = (255, 244, 234)
                    sideColour = (235, 238, 211)
                    for button in button_list:
                        button.changeMode(font, backgroundColour, lmt, lmtc)

                if button_list[1].rect.collidepoint(pos):
                    close_button = changeColour(close_button, textColour[0], textColour[1], textColour[2])
                    settingsPage.colour = (71, 60, 68)
                    settingsPage.updateColour((71, 60, 68))
                    backgroundColour = (71, 60, 68)
                    sideColour = (55, 51, 60)
                    for button in button_list:
                        button.changeMode(font, backgroundColour, dmt, dmtc)

                if button_list[3].rect.collidepoint(pos):
                    cursor_value = 0
                    adj = 10
                if button_list[4].rect.collidepoint(pos):
                    cursor_value = 1
                    adj = 10
                if button_list[5].rect.collidepoint(pos):
                    cursor_value = 2
                    adj = 0
                if button_list[7].rect.collidepoint(pos):
                    done = True
                    windim_pressed = True
                    winDim = (600, 400)
                    # sidebar(winDim, True, backgroundColour, sideColour)
                if button_list[8].rect.collidepoint(pos):
                    done = True
                    windim_pressed = True
                    winDim = (900, 600)
                    # sidebar(winDim, True, backgroundColour, sideColour)

                if button_list[9].rect.collidepoint(pos):
                    done = True
                    windim_pressed = True
                    winDim = (1200, 800)
                    # sidebar(winDim, True, backgroundColour, sideColour)

                if button_list[11].rect.collidepoint(pos):
                    data.value = 0
                if button_list[12].rect.collidepoint(pos):
                    data.value = 1


                if close_rect.collidepoint(pos):
                    done = True

                if done == True:
                    settingsPage.open = False
                    circles_visible = True
                    rect_can_be_clicked = True
                    settingsPage.fillWindow(0)
            # circleBgColour = circleBackground(settingsPage.colour)

        pygame.mouse.set_visible(False)
        window.blit(cursor_list[cursor_value], (pygame.mouse.get_pos()[0] - adj, pygame.mouse.get_pos()[1] - adj))

        pygame.display.flip()
        # for button in button_list:
        #     button.reset(font)

    return backgroundColour, backgroundColour, sideColour, cursor_value, adj, winDim, circles_visible, rect_can_be_clicked, windim_pressed