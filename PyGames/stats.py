import pygame
from colors import colors, text_color
import random
import json


def show_stats(screen, clock):
    viewing = True

    with open("high_scores.json", "r") as file:
        data = json.load(file)

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx

    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)

    menu_title_font = pygame.font.SysFont("Arial", 50, bold=True)
    subheading_font = pygame.font.SysFont("Arial", 32, bold=True)
    stats_font = pygame.font.SysFont("Arial", 26)

    subheading_color = random.choice(colors)
    stats_color = "white"

    menu_title_surface = menu_title_font.render("GAME STATS", True, "white")
    menu_title_rect = menu_title_surface.get_rect()
    menu_title_rect.centerx = center_x
    menu_title_rect.y = 60

    breakout_title_surface = subheading_font.render("BREAKOUT", True, subheading_color)
    breakout_title_rect = breakout_title_surface.get_rect()
    breakout_title_rect.centerx = center_x
    breakout_title_rect.y = 150

    breakout_hs_text = f"High Score: {data['breakout']['high_score']}"
    breakout_hs_surface = stats_font.render(breakout_hs_text, True, stats_color)
    breakout_hs_rect = breakout_hs_surface.get_rect()
    breakout_hs_rect.centerx = center_x
    breakout_hs_rect.y = 190

    dino_title_surface = subheading_font.render("DINO GAME", True, subheading_color)
    dino_title_rect = dino_title_surface.get_rect()
    dino_title_rect.centerx = center_x
    dino_title_rect.y = 240

    dino_hs_text = f"High Score: {data['dino']['high_score']}"
    dino_hs_surface = stats_font.render(dino_hs_text, True, stats_color)
    dino_hs_rect = dino_hs_surface.get_rect()
    dino_hs_rect.centerx = center_x
    dino_hs_rect.y = 280

    space_title_surface = subheading_font.render("SPACE INVADERS", True, subheading_color)
    space_title_rect = space_title_surface.get_rect()
    space_title_rect.centerx = center_x
    space_title_rect.y = 330

    space_hs_text = f"High Score: {data['space_invaders']['high_score']}"
    space_hs_surface = stats_font.render(space_hs_text, True, stats_color)
    space_hs_rect = space_hs_surface.get_rect()
    space_hs_rect.centerx = center_x
    space_hs_rect.y = 370

    ttt_title_surface = subheading_font.render("TIC TAC TOE", True, subheading_color)
    ttt_title_rect = ttt_title_surface.get_rect()
    ttt_title_rect.centerx = center_x
    ttt_title_rect.y = 420

    ttt_wins_text = f"Wins: {data['tic_tac_toe']['wins']}"
    ttt_wins_surface = stats_font.render(ttt_wins_text, True, stats_color)
    ttt_wins_rect = ttt_wins_surface.get_rect()
    ttt_wins_rect.centerx = center_x
    ttt_wins_rect.y = 460

    ttt_losses_text = f"Losses: {data['tic_tac_toe']['losses']}"
    ttt_losses_surface = stats_font.render(ttt_losses_text, True, stats_color)
    ttt_losses_rect = ttt_losses_surface.get_rect()
    ttt_losses_rect.centerx = center_x
    ttt_losses_rect.y = 490

    ttt_ties_text = f"Ties: {data['tic_tac_toe']['ties']}"
    ttt_ties_surface = stats_font.render(ttt_ties_text, True, stats_color)
    ttt_ties_rect = ttt_ties_surface.get_rect()
    ttt_ties_rect.centerx = center_x
    ttt_ties_rect.y = 520

    return_color = random.choice(colors)
    return_text_color = text_color(return_color)

    return_button = pygame.Rect(0, 0, 270, 50)
    return_button.centerx = center_x
    return_button.y = 600

    return_text = stats_font.render("Resume Game", True, return_text_color)
    return_text_rect = return_text.get_rect()
    return_text_rect.center = return_button.center

    while viewing:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_button.collidepoint(event.pos):
                    return "return"

        screen.blit(overlay, (0, 0))

        screen.blit(menu_title_surface, menu_title_rect)
        screen.blit(breakout_title_surface, breakout_title_rect)
        screen.blit(dino_title_surface, dino_title_rect)
        screen.blit(space_title_surface, space_title_rect)
        screen.blit(ttt_title_surface, ttt_title_rect)

        screen.blit(breakout_hs_surface, breakout_hs_rect)
        screen.blit(dino_hs_surface, dino_hs_rect)
        screen.blit(space_hs_surface, space_hs_rect)

        screen.blit(ttt_wins_surface, ttt_wins_rect)
        screen.blit(ttt_losses_surface, ttt_losses_rect)
        screen.blit(ttt_ties_surface, ttt_ties_rect)

        pygame.draw.rect(screen, return_color, return_button)
        screen.blit(return_text, return_text_rect)

        pygame.display.flip()
        clock.tick(60)