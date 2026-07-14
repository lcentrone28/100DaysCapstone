import pygame
import PyGames.pause as pause
from colors import colors, text_color
import random

def init_aliens(rows, cols, x_start, y_start, w, h, x_space, y_space):
    alien_list = []
    for row in range(rows):
        for col in range(cols):
            ax = x_start + col * (w + x_space)
            ay = y_start + row * (h + y_space)
            alien_list.append(pygame.Rect(ax, ay, w, h))
    return alien_list


def run_space(screen, clock):
    running = True

    current_screen = "level start"
    next_level_target = "lvl 1"
    level_start_timer = pygame.time.get_ticks()
    level_start_duration = 2000

    score = 0
    health = 100

    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    text_font = pygame.font.SysFont("Arial", 30)

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx

    replay_color = random.choice(colors)
    menu_color = random.choice(colors)

    replay_text_color = text_color(replay_color)
    menu_text_color = text_color(menu_color)

    get_colors = random.sample(colors, 12)

    assign_colors = {
        'player': get_colors[0],
        'enemy1': get_colors[1],
        'enemy2': get_colors[2],
        'enemy3': get_colors[3],
        'p_fire': get_colors[4],
        'e_fire1': get_colors[5],
        'e_fire2': get_colors[6],
        'e_fire3': get_colors[7],
        'score_title': get_colors[8],
        'score_text': get_colors[9],
        'health_title': get_colors[10],
        'health_text': get_colors[11]
    }

    player_color = assign_colors['player']
    e1_color = assign_colors['enemy1']
    e2_color = assign_colors['enemy2']
    e3_color = assign_colors['enemy3']
    pf_color = assign_colors['p_fire']
    ef1_color = assign_colors['e_fire1']
    ef2_color = assign_colors['e_fire2']
    ef3_color = assign_colors['e_fire3']
    score_title_color = assign_colors['score_title']
    score_color = assign_colors['score_text']
    health_title_color = assign_colors['health_title']
    health_color = assign_colors['health_text']

    player_width = 50
    player_height = 30
    player_speed = 6
    player = pygame.Rect(center_x - player_width // 2, screen_rect.height - 70, player_width, player_height)

    alien_w = 40
    alien_h = 30
    x_spacing = 20
    y_spacing = 20
    grid_start_x = 100
    grid_start_y = 100

    aliens = init_aliens(3, 6, grid_start_x, grid_start_y, alien_w, alien_h, x_spacing, y_spacing)

    alien_direction = 1
    alien_speed = 2
    alien_move_down_distance = 25

    player_lasers = []
    alien_lasers = []
    laser_speed = 7
    l_cooldown = 25
    l_state = 0

    replay_button = pygame.Rect(0, 0, 350, 50)
    menu_button = pygame.Rect(0, 0, 350, 50)

    replay_button.centerx = center_x
    menu_button.centerx = center_x
    replay_button.y = 320
    menu_button.y = 400

    score_title_text = text_font.render("Score:", True, score_title_color)
    score_title_text_rect = score_title_text.get_rect()
    score_title_text_rect.topleft = (80, 50)

    health_title_text = text_font.render("Health:", True, health_title_color)
    health_title_text_rect = health_title_text.get_rect()

    replay_text = text_font.render("Replay?", True, replay_text_color)
    replay_text_rect = replay_text.get_rect()
    replay_text_rect.center = replay_button.center

    menu_text = text_font.render("Back to Main Menu", True, menu_text_color)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = menu_button.center

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True

                while paused:
                    choice = pause.pause_game(screen, clock)

                    if choice == "resume":
                        paused = False
                    elif choice == "back":
                        choice = pause.warning(screen, clock)
                        if choice == "exit":
                            return "back"
                    elif choice == "quit":
                        choice = pause.warning(screen, clock)
                        if choice == "exit":
                            return "quit"
                    elif choice == "stats":
                        return "stats"

            if current_screen in ["lvl 1", "lvl 2", "lvl 3"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if l_state == 0:
                        lw, lh = 4, 15
                        lx = player.centerx - lw // 2
                        ly = player.top - lh
                        player_lasers.append(pygame.Rect(lx, ly, lw, lh))
                        l_state = l_cooldown

            elif current_screen in ["game over", "game won"]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if replay_button.collidepoint(event.pos):
                        score = 0
                        health = 100
                        player_lasers.clear()
                        alien_lasers.clear()
                        player.centerx = center_x
                        alien_direction = 1
                        l_state = 0
                        aliens = init_aliens(3, 6, grid_start_x, grid_start_y, alien_w, alien_h, x_spacing, y_spacing)
                        next_level_target = "lvl 1"
                        level_start_timer = pygame.time.get_ticks()
                        current_screen = "level start"
                    elif menu_button.collidepoint(event.pos):
                        return "back"

        if current_screen == "level start":
            if pygame.time.get_ticks() - level_start_timer >= level_start_duration:
                current_screen = next_level_target

        if current_screen in ["lvl 1", "lvl 2", "lvl 3"]:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= player_speed
                if player.left < 0:
                    player.left = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += player_speed
                if player.right > screen_rect.width:
                    player.right = screen_rect.width

            if current_screen == "lvl 2":
                alien_speed = 3
                alien_move_down_distance = 30
                laser_speed = 10
                l_cooldown = 17
            elif current_screen == "lvl 3":
                alien_speed = 4
                alien_move_down_distance = 35
                laser_speed = 12
                l_cooldown = 13

            if l_state > 0:
                l_state -= 1

            for laser in player_lasers[:]:
                laser.y -= laser_speed
                if laser.bottom < 0:
                    player_lasers.remove(laser)

            shift_down = False

            for alien in aliens:
                alien.x += alien_speed * alien_direction
                if alien.right >= screen_rect.width or alien.left <= 0:
                    shift_down = True

            if shift_down:
                alien_direction *= -1

                for alien in aliens:
                    alien.y += alien_move_down_distance
                    if alien.bottom >= player.top:
                        current_screen = "game over"

            if aliens and random.randint(1, 100) < 3:
                shooting_alien = random.choice(aliens)
                al_w, al_h = 4, 15
                al_x = shooting_alien.centerx - al_w // 2
                al_y = shooting_alien.bottom
                alien_lasers.append(pygame.Rect(al_x, al_y, al_w, al_h))

            for laser in alien_lasers[:]:
                laser.y += laser_speed

                if laser.top > screen_rect.height:
                    alien_lasers.remove(laser)
                elif laser.colliderect(player):
                    alien_lasers.remove(laser)

                    if current_screen == "lvl 1":
                        health -= 10
                    elif current_screen == "lvl 2":
                        health -= 15
                    elif current_screen == "lvl 3":
                        health -= 25

                    if health <= 0:
                        health = 0
                        current_screen = "game over"

            for p_laser in player_lasers[:]:
                hit_detected = False

                for alien in aliens[:]:
                    if p_laser.colliderect(alien):
                        aliens.remove(alien)
                        player_lasers.remove(p_laser)

                        if current_screen == "lvl 1":
                            score += 10
                        elif current_screen == "lvl 2":
                            score += 20
                        elif current_screen == "lvl 3":
                            score += 30

                        hit_detected = True
                        break

                if hit_detected:
                    continue

            if len(aliens) == 0:
                player_lasers.clear()
                alien_lasers.clear()
                player.centerx = center_x
                alien_direction = 1

                if current_screen == "lvl 1":
                    aliens = init_aliens(4, 7, grid_start_x, grid_start_y, alien_w, alien_h, x_spacing, y_spacing)
                    next_level_target = "lvl 2"
                    level_start_timer = pygame.time.get_ticks()
                    current_screen = "level start"
                elif current_screen == "lvl 2":
                    aliens = init_aliens(5, 8, grid_start_x, grid_start_y, alien_w, alien_h, x_spacing, y_spacing)
                    next_level_target = "lvl 3"
                    level_start_timer = pygame.time.get_ticks()
                    current_screen = "level start"
                elif current_screen == "lvl 3":
                    current_screen = "game won"

        screen.fill("black")

        if current_screen in ["lvl 1", "lvl 2", "lvl 3"]:
            pygame.draw.rect(screen, player_color, player)

            for laser in player_lasers:
                pygame.draw.rect(screen, pf_color, laser)

            for alien in aliens:
                if current_screen == "lvl 1":
                    pygame.draw.rect(screen, e1_color, alien)
                elif current_screen == "lvl 2":
                    pygame.draw.rect(screen, e2_color, alien)
                elif current_screen == "lvl 3":
                    pygame.draw.rect(screen, e3_color, alien)

            for laser in alien_lasers:
                if current_screen == "lvl 1":
                    pygame.draw.rect(screen, ef1_color, laser)
                elif current_screen == "lvl 2":
                    pygame.draw.rect(screen, ef2_color, laser)
                elif current_screen == "lvl 3":
                    pygame.draw.rect(screen, ef3_color, laser)

            score_text = text_font.render(f"{score}", True, score_color)
            score_text_rect = score_text.get_rect()
            score_text_rect.topleft = (score_title_text_rect.right + 10, 50)

            screen.blit(score_title_text, score_title_text_rect)
            screen.blit(score_text, score_text_rect)

            health_text = text_font.render(f"{health}", True, health_color)
            health_text_rect = health_text.get_rect()

            health_text_rect.topright = (screen_rect.width - 80, 50)
            health_title_text_rect.topright = (health_text_rect.left - 10, 50)

            screen.blit(health_title_text, health_title_text_rect)
            screen.blit(health_text, health_text_rect)

        elif current_screen == "level start":
            display_num = next_level_target[-1]
            level_start_text = title_font.render(f"LEVEL {display_num}", True, "white")
            screen.blit(level_start_text, (center_x - level_start_text.get_width() // 2,
                                           screen_rect.centery - level_start_text.get_height() // 2))

        elif current_screen in ["game over", "game won"]:
            msg = "You Win" if current_screen == "game won" else "Game Over"
            title_surface = title_font.render(msg, True, "white")
            screen.blit(title_surface, (center_x - title_surface.get_width() // 2, 200))

            pygame.draw.rect(screen, replay_color, replay_button)
            pygame.draw.rect(screen, menu_color, menu_button)

            screen.blit(replay_text, replay_text_rect)
            screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)

    return "back"