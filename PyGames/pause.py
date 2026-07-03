import pygame
import colors
import random
import stats

def pause_game(screen, clock):
    paused = True

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx

    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)

    menu_title_font = pygame.font.SysFont("Arial", 50, bold=True)
    menu_title_surface = menu_title_font.render("PAUSED", True, "white")

    button_font = pygame.font.SysFont("Arial", 30)

    resume_color = random.choice(colors.colors)
    back_color = random.choice(colors.colors)
    quit_color = random.choice(colors.colors)
    stats_color = random.choice(colors.colors)

    resume_text_color = colors.text_color(resume_color)
    back_text_color = colors.text_color(back_color)
    quit_text_color = colors.text_color(quit_color)
    stats_text_color = colors.text_color(stats_color)

    menu_title_rect = menu_title_surface.get_rect()
    menu_title_rect.centerx = center_x
    menu_title_rect.y = 200

    resume_button = pygame.Rect(0, 0, 350, 50)
    back_button = pygame.Rect(0, 0, 350, 50)
    quit_button = pygame.Rect(0, 0, 350, 50)
    stats_button = pygame.Rect(0, 0, 350, 50)

    resume_button.centerx = center_x
    back_button.centerx = center_x
    quit_button.centerx = center_x
    stats_button.centerx = center_x

    resume_button.y = 300
    back_button.y = 370
    quit_button.y = 440
    stats_button.y = 510

    resume_text = button_font.render("Resume", True, resume_text_color)
    resume_text_rect = resume_text.get_rect()
    resume_text_rect.center = resume_button.center

    back_text = button_font.render("Back to Main Menu", True, back_text_color)
    back_text_rect = back_text.get_rect()
    back_text_rect.center = back_button.center

    quit_text = button_font.render("Quit Program", True, quit_text_color)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = quit_button.center

    stats_text = button_font.render("View Game Stats", True, stats_text_color)
    stats_text_rect = stats_text.get_rect()
    stats_text_rect.center = stats_button.center

    while paused:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.collidepoint(event.pos):
                    return "resume"
                elif back_button.collidepoint(event.pos):
                    return "back"
                elif quit_button.collidepoint(event.pos):
                    return "quit"
                elif stats_button.collidepoint(event.pos):
                    selection = stats.show_stats(screen, clock)

                    if selection == "return":
                        return "resume"

        screen.blit(overlay, (0, 0))

        screen.blit(menu_title_surface, menu_title_rect)

        pygame.draw.rect(screen, resume_color, resume_button)
        pygame.draw.rect(screen, back_color, back_button)
        pygame.draw.rect(screen, quit_color, quit_button)
        pygame.draw.rect(screen, stats_color, stats_button)

        screen.blit(resume_text, resume_text_rect)
        screen.blit(back_text, back_text_rect)
        screen.blit(quit_text, quit_text_rect)
        screen.blit(stats_text, stats_text_rect)

        pygame.display.flip()
        clock.tick(60)

def warning(screen, clock):
    exit_triggered = True

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx

    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)

    menu_title_font = pygame.font.SysFont("Arial", 40, bold=True)
    menu_title_surface = menu_title_font.render("Are you sure you would like to exit?", True, "white")

    menu_desc_font = pygame.font.SysFont("Arial", 35, italic=True)
    menu_desc_surface = menu_desc_font.render("All progress will be lost.", True, "white")

    button_font = pygame.font.SysFont("Arial", 30)

    resume_color = random.choice(colors.greens)
    quit_color = random.choice(colors.reds)

    resume_text_color = colors.text_color(resume_color)
    quit_text_color = colors.text_color(quit_color)

    menu_title_rect = menu_title_surface.get_rect()
    menu_title_rect.centerx = center_x
    menu_title_rect.y = 200

    menu_desc_rect = menu_desc_surface.get_rect()
    menu_desc_rect.centerx = center_x
    menu_desc_rect.y = 260

    resume_button = pygame.Rect(0, 0, 350, 50)
    quit_button = pygame.Rect(0, 0, 350, 50)

    resume_button.centerx = center_x
    quit_button.centerx = center_x

    resume_button.y = 340
    quit_button.y = 410

    resume_text = button_font.render("No, Go Back", True, resume_text_color)
    resume_text_rect = resume_text.get_rect()
    resume_text_rect.center = resume_button.center

    quit_text = button_font.render("Yes, Exit", True, quit_text_color)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = quit_button.center

    while exit_triggered:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.collidepoint(event.pos):
                    return "resume"
                elif quit_button.collidepoint(event.pos):
                    return "exit"

        screen.blit(overlay, (0, 0))

        screen.blit(menu_title_surface, menu_title_rect)
        screen.blit(menu_desc_surface, menu_desc_rect)

        pygame.draw.rect(screen, resume_color, resume_button)
        pygame.draw.rect(screen, quit_color, quit_button)

        screen.blit(resume_text, resume_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
        clock.tick(60)