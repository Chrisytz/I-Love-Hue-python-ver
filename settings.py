import pygame

def changeColour(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue
    return surface

def settings(win_vars, current_cursor, textHoverColour, textColour, settingColour,
          sidebarColour, window, event, adj, winsize, settingsPage, circles_visible, rect_can_be_clicked, cursor_list):
    pygame.init()
    win_size = winsize
    window = pygame.display.set_mode((win_size))
    pygame.display.set_caption("SETTINGGSSSADAD")

    done = False

    font = pygame.font.Font('Quicksand-Regular.ttf', int(win_vars["font_size"]))
    # button_list = [lightMode, darkMode, circle, x, arrow]
    cursor_value = current_cursor
    pos = pygame.mouse.get_pos()
    backgroundColour = settingColour
    sideColour = sidebarColour
    backgroundValue = None
    winDim = win_size

    line1 = "LIGHT MODE"
    line2 = "DARK MODE"

    line4 = ["WINDOW SIZE:", "600 x 400", "900 x 600", "1200 x 800"]

    line1_button = font.render("LIGHT MODE", True, textColour, backgroundColour)
    line2_button = font.render("DARK MODE", True, textColour, backgroundColour)
    line3_button = [font.render("CURSOR:", True, textColour, backgroundColour),
                    pygame.transform.smoothscale(pygame.image.load('circle.png').convert_alpha(), (int(win_vars["sprite_size"] / 2.5), int(win_vars["sprite_size"] / 2.5))),
                    pygame.transform.smoothscale(pygame.image.load('x.png').convert_alpha(), (int(win_vars["sprite_size"] / 2.5), int(win_vars["sprite_size"] / 2.5))),
                    pygame.transform.smoothscale(pygame.image.load('cursor.png').convert_alpha(), (int(win_vars["sprite_size"] / 2.5), int(win_vars["sprite_size"] / 2.5)))]
    line3_button[1:4] = [changeColour(x, textColour[0], textColour[1], textColour[2]) for x in line3_button[1:4]]

    line4_button = [font.render(x, True, textColour, backgroundColour) for x in line4]

    close_button = changeColour(pygame.transform.smoothscale(pygame.image.load('x.png').convert_alpha(), (int(win_vars["sprite_size"] / 2), int(win_vars["sprite_size"] / 2))),
                                textColour[0], textColour[1], textColour[2])

    line1_rect = line1_button.get_rect(
        topleft=(win_vars["sprite_size"], win_vars["sprite_size"] * 1.2))
    line2_rect = line2_button.get_rect(
        topleft=(win_vars["sprite_size"], line1_rect.bottomright[1] + win_vars["sprite_size"]))
    line3_rect = [line3_button[0].get_rect(
        topleft=(win_vars["sprite_size"], line2_rect.bottomright[1] + win_vars["sprite_size"]))]

    for cursor in line3_button[1:4]:
        line3_rect.append(cursor.get_rect(topleft=(
            win_vars["sprite_size"] / 1.5 + line3_rect[line3_button.index(cursor) - 1].topright[0],
            line2_rect.bottomright[1] + win_vars["sprite_size"]*1.1)))

    line4_rect = [line4_button[0].get_rect(
        topleft=(win_vars["sprite_size"], line3_rect[0].bottomright[1] + win_vars["sprite_size"]))]

    for size in line4_button[1:4]:
        line4_rect.append(size.get_rect(topleft=(
            win_vars["sprite_size"] / 1.5 + line4_rect[line4_button.index(size) - 1].topright[0],
            line3_rect[0].bottomright[1] + win_vars["sprite_size"])))

    close_rect = close_button.get_rect(topleft = (win_vars["sprite_size"]/4, win_vars["sprite_size"]/4))



    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            while line1_rect.collidepoint(pos):
                textColour = textHoverColour
                on_hover = font.render(line1, True, textColour, backgroundColour)
                window.blit(on_hover, line1_rect)

            while line2_rect.collidepoint(pos):
                textColour = textHoverColour
                on_hover = font.render(line2, True, textColour, backgroundColour)
                window.blit(on_hover, line2_rect)

            for cursor in line3_rect[1:4]:
                while cursor.collidepoint(pos):
                    print ("collided!")
                    on_hover = changeColour(line3_button[line3_rect.index(cursor)], textHoverColour[0], textHoverColour[1], textHoverColour[2])
                    window.blit(on_hover, cursor)

            for button in line4_rect[1:4]:
                while button.collidepoint(pos):
                    textColour = textHoverColour
                    on_hover = font.render(line4[line4_rect.index(button)], True, textColour, backgroundColour)
                    window.blit(on_hover, button)
            while close_rect.collidepoint(pos):
                on_hover = changeColour(close_button, textHoverColour[0], textHoverColour[1],
                                        textHoverColour[2])
                window.blit(on_hover, close_rect)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if line1_rect.collidepoint(pos):
                    backgroundColour = (255, 244, 234)
                    sideColour = (235, 238, 211)

                if line2_rect.collidepoint(pos):
                    backgroundColour = (71, 60, 68)
                    sideColour = (55, 51, 60)

                if line3_rect[1].collidepoint(pos):
                    cursor_value = 0
                    adj = 10
                if line3_rect[2].collidepoint(pos):
                    cursor_value = 1
                    adj = 10
                if line3_rect[3].collidepoint(pos):
                    cursor_value = 2
                    adj = 0
                if line4_rect[1].collidepoint(pos):
                    winDim = (600, 400)
                    # sidebar(winDim, True, backgroundColour, sideColour)
                if line4_rect[2].collidepoint(pos):
                    winDim = (900, 600)
                    # sidebar(winDim, True, backgroundColour, sideColour)

                if line4_rect[3].collidepoint(pos):
                    winDim = (1200, 800)
                    # sidebar(winDim, True, backgroundColour, sideColour)

                if close_rect.collidepoint(pos):
                    done = True
                    settingsPage.open = False
                    circles_visible = True
                    rect_can_be_clicked = True
                    settingsPage.fillWindow(0)
                    pygame.quit()

        settingsPage.updateColour()
            # circleBgColour = circleBackground(settingsPage.colour)

        window.blit(settingsPage.image, (0, 0, win_size[0], win_size[1]))

        window.blit(line1_button, line1_rect)
        window.blit(line2_button, line2_rect)

        for x in line3_button:
            window.blit(x, line3_rect[line3_button.index(x)])

        for x in line4_button:
            window.blit(x, line4_rect[line4_button.index(x)])

        window.blit(close_button, close_rect)

        settingsPage.updateColour()

        pygame.mouse.set_visible(False)
        window.blit(cursor_list[cursor_value], (pygame.mouse.get_pos()[0] - adj, pygame.mouse.get_pos()[1] - adj))

        pygame.display.flip()

    return backgroundColour, backgroundColour, sideColour, cursor_value, adj, winDim, circles_visible, rect_can_be_clicked