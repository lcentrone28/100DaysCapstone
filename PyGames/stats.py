import pygame
from colors import colors, text_color
import random
import json

def show_stats(screen, clock):
    viewing = True

    with open("stats.json", "r") as file:
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

    breakout_stats = [
        f"High Score: {data['breakout']['high_score']}"
    ]
    breakout_start_y = 190
    breakout_spacing = 30

    dino_title_surface = subheading_font.render("DINO GAME", True, subheading_color)
    dino_title_rect = dino_title_surface.get_rect()
    dino_title_rect.centerx = center_x
    dino_title_rect.y = 240

    dino_stats = [
        f"High Score: {data['dino']['high_score']}"
    ]
    dino_start_y = 280
    dino_spacing = 30

    space_title_surface = subheading_font.render("SPACE INVADERS", True, subheading_color)
    space_title_rect = space_title_surface.get_rect()
    space_title_rect.centerx = center_x
    space_title_rect.y = 330

    space_stats = [
        f"High Score: {data['space_invaders']['high_score']}"
    ]
    space_start_y = 370
    space_spacing = 30

    ttt_title_surface = subheading_font.render("TIC TAC TOE", True, subheading_color)
    ttt_title_rect = ttt_title_surface.get_rect()
    ttt_title_rect.centerx = center_x
    ttt_title_rect.y = 420

    ttt_stats = [
        ("Player V Comp.", "Player V Player"),
        (f"Wins: {data['tic_tac_toe']['single_player']['wins']}", f"Wins: {data['tic_tac_toe']['multiplayer']['wins']}"),
        (f"Losses: {data['tic_tac_toe']['single_player']['losses']}", f"Losses: {data['tic_tac_toe']['multiplayer']['losses']}"),
        (f"Ties: {data['tic_tac_toe']['single_player']['ties']}", f"Ties: {data['tic_tac_toe']['multiplayer']['ties']}")
    ]
    ttt_start_y = 460
    ttt_spacing = 30
    column_offset = 120

    return_color = random.choice(colors)
    return_text_color = text_color(return_color)

    return_button = pygame.Rect(0, 0, 270, 50)
    return_button.centerx = center_x
    return_button.y = 620

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

        for index, line_text in enumerate(breakout_stats):
            line_surface = stats_font.render(line_text, True, stats_color)
            line_rect = line_surface.get_rect()
            line_rect.centerx = center_x
            line_rect.y = breakout_start_y + (index * breakout_spacing)
            screen.blit(line_surface, line_rect)

        for index, line_text in enumerate(dino_stats):
            line_surface = stats_font.render(line_text, True, stats_color)
            line_rect = line_surface.get_rect()
            line_rect.centerx = center_x
            line_rect.y = dino_start_y + (index * dino_spacing)
            screen.blit(line_surface, line_rect)

        for index, line_text in enumerate(space_stats):
            line_surface = stats_font.render(line_text, True, stats_color)
            line_rect = line_surface.get_rect()
            line_rect.centerx = center_x
            line_rect.y = space_start_y + (index * space_spacing)
            screen.blit(line_surface, line_rect)

        for index, (pvc_text, pvp_text) in enumerate(ttt_stats):
            pvc_surface = stats_font.render(pvc_text, True, stats_color)
            pvc_rect = pvc_surface.get_rect()
            pvc_rect.centerx = center_x - column_offset
            pvc_rect.y = ttt_start_y + (index * ttt_spacing)
            screen.blit(pvc_surface, pvc_rect)

            pvp_surface = stats_font.render(pvp_text, True, stats_color)
            pvp_rect = pvp_surface.get_rect()
            pvp_rect.centerx = center_x + column_offset
            pvp_rect.y = ttt_start_y + (index * ttt_spacing)
            screen.blit(pvp_surface, pvp_rect)

        pygame.draw.rect(screen, return_color, return_button)
        screen.blit(return_text, return_text_rect)

        pygame.display.flip()
        clock.tick(60)