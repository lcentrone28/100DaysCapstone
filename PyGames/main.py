import pygame
import sys
import os
os.environ['SDL_MOUSE_FOCUS_CLICKTHROUGH'] = '1'
import random

import games.breakout as breakout
import games.dino as dino
import games.space as space
import games.tictactoe as ttt
import pause
from colors import colors, text_color

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
is_paused = False

current_screen = "menu"

screen_rect = screen.get_rect()
center_x = screen_rect.centerx

menu_title_font = pygame.font.SysFont("Arial", 50, bold=True)
menu_title_surface = menu_title_font.render("MINIGAMES", True, "white")

button_font = pygame.font.SysFont("Arial", 30)

breakout_color = random.choice(colors)
dino_color = random.choice(colors)
space_color = random.choice(colors)
ttt_color = random.choice(colors)

breakout_text_color = text_color(breakout_color)
dino_text_color = text_color(dino_color)
space_text_color = text_color(space_color)
ttt_text_color = text_color(ttt_color)

menu_title_rect = menu_title_surface.get_rect()
menu_title_rect.centerx = center_x
menu_title_rect.y = 200

breakout_button = pygame.Rect(0, 0, 270, 50)
dino_button = pygame.Rect(0, 0, 270, 50)
space_button = pygame.Rect(0, 0, 270, 50)
ttt_button = pygame.Rect(0, 0, 270, 50)

breakout_button.centerx = center_x
dino_button.centerx = center_x
space_button.centerx = center_x
ttt_button.centerx = center_x

breakout_button.y = 300
dino_button.y = 370
space_button.y = 440
ttt_button.y = 510

breakout_text = button_font.render("Breakout", True, breakout_text_color)
breakout_text_rect = breakout_text.get_rect()
breakout_text_rect.center = breakout_button.center

dino_text = button_font.render("Dino Game", True, dino_text_color)
dino_text_rect = dino_text.get_rect()
dino_text_rect.center = dino_button.center

space_text = button_font.render("Space Invaders", True, space_text_color)
space_text_rect = space_text.get_rect()
space_text_rect.center = space_button.center

ttt_text = button_font.render("Tic Tac Toe", True, ttt_text_color)
ttt_text_rect = ttt_text.get_rect()
ttt_text_rect.center = ttt_button.center

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            choice = pause.warning(screen, clock)
            if choice == "exit":
                running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            choice = pause.warning(screen, clock)
            if choice == "exit":
                running = False

        if current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if breakout_button.collidepoint(event.pos):
                    current_screen = "breakout"
                elif dino_button.collidepoint(event.pos):
                    current_screen = "dino"
                elif space_button.collidepoint(event.pos):
                    current_screen = "space"
                elif ttt_button.collidepoint(event.pos):
                    current_screen = "ttt"

    screen.fill("black")

    if current_screen == "menu":
        screen.blit(menu_title_surface, menu_title_rect)

        pygame.draw.rect(screen, breakout_color, breakout_button)
        pygame.draw.rect(screen, dino_color, dino_button)
        pygame.draw.rect(screen, space_color, space_button)
        pygame.draw.rect(screen, ttt_color, ttt_button)

        screen.blit(breakout_text, breakout_text_rect)
        screen.blit(dino_text, dino_text_rect)
        screen.blit(space_text, space_text_rect)
        screen.blit(ttt_text, ttt_text_rect)

    elif current_screen == "breakout":
        game_choice = breakout.run_breakout(screen, clock)

        if game_choice == "back":
            current_screen = "menu"
        elif game_choice == "quit":
            running = False

    elif current_screen == "dino":
        game_choice = dino.run_dino(screen, clock)

        if game_choice == "back":
            current_screen = "menu"
        elif game_choice == "quit":
            running = False

    elif current_screen == "space":
        game_choice = space.run_space(screen, clock)

        if game_choice == "back":
            current_screen = "menu"
        elif game_choice == "quit":
            running = False

    elif current_screen == "ttt":
        game_choice = ttt.run_ttt(screen, clock)

        if game_choice == "back":
            current_screen = "menu"
        elif game_choice == "quit":
            running = False

    pygame.display.flip()
    clock.tick(60)
sys.exit()