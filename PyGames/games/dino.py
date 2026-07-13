import pygame
import PyGames.pause as pause
from colors import colors, text_color
import random

def get_x(target_x, existing_obstacles, min_distance=220):
    while any(abs(target_x - obs.x) < min_distance for obs in existing_obstacles):
        target_x += random.randint(200, 400)
    return target_x

def run_dino(screen, clock):
    running = True

    current_screen = "opening"
    true_score = 0
    c1_cleared = False
    c2_cleared = False
    tc1_cleared = False
    tc2_cleared = False
    pt_cleared = False
    tc1_spawns = 1
    tc2_spawns = 0
    pt_spawns = 0

    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    text_font = pygame.font.SysFont("Arial", 30)

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx
    ground_y = screen_rect.height - 300

    replay_color = random.choice(colors)
    menu_color = random.choice(colors)

    replay_text_color = text_color(replay_color)
    menu_text_color = text_color(menu_color)

    get_colors = random.sample(colors, 8)

    assign_colors = {
        'player': get_colors[0],
        'cactus1': get_colors[1],
        'cactus2': get_colors[2],
        'tall_cactus1': get_colors[3],
        'tall_cactus2': get_colors[4],
        'pterodactyl': get_colors[5],
        'score_title': get_colors[6],
        'score_text': get_colors[7]
    }

    player_color = assign_colors['player']
    c1_color = assign_colors['cactus1']
    c2_color = assign_colors['cactus2']
    tc1_color = assign_colors['tall_cactus1']
    tc2_color = assign_colors['tall_cactus2']
    pt_color = assign_colors['pterodactyl']
    score_title_color = assign_colors['score_title']
    score_color = assign_colors['score_text']

    ground = pygame.Rect(0, ground_y, screen_rect.width, 5)
    player = pygame.Rect(50, ground_y - 40, 40, 40)

    pt_spawn_height = [ground_y - 60, ground_y - 75, ground_y - 120]
    chosen_y = random.choice(pt_spawn_height)

    c1 = pygame.Rect(get_x(screen_rect.width + random.randint(0, 1200), []), ground_y - 60, 30, 60)
    obstacles = [c1]

    x2 = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
    c2 = pygame.Rect(x2, ground_y - 60, 30, 60)
    obstacles.append(c2)

    xtc1 = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
    tc1 = pygame.Rect(xtc1, ground_y - 90, 30, 90)
    obstacles.append(tc1)

    xtc2 = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
    tc2 = pygame.Rect(xtc2, ground_y - 90, 30, 90)
    obstacles.append(tc2)

    xpt = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
    pt = pygame.Rect(xpt, chosen_y, 40, 40)
    obstacles.append(pt)

    player_velocity_y = 0
    gravity = 1
    jump_count = 0

    replay_button = pygame.Rect(0, 0, 350, 50)
    menu_button = pygame.Rect(0, 0, 350, 50)

    replay_button.centerx = center_x
    menu_button.centerx = center_x
    replay_button.y = 320
    menu_button.y = 400

    score_title_text = text_font.render("Score:", True, score_title_color)
    score_title_text_rect = score_title_text.get_rect()
    score_title_text_rect.topleft = (80, 50)

    replay_text = text_font.render("Replay?", True, replay_text_color)
    replay_text_rect = replay_text.get_rect()
    replay_text_rect.center = replay_button.center

    menu_text = text_font.render("Back to Main Menu", True, menu_text_color)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = menu_button.center

    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

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

            if current_screen == "opening":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_screen = "playing"

            elif current_screen == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if jump_count < 3 and not keys[pygame.K_DOWN]:
                        player_velocity_y = -17
                        jump_count += 1

            elif current_screen == "game over":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if replay_button.collidepoint(event.pos):
                        true_score = 0
                        pt_spawns = 0
                        tc1_spawns = 0
                        tc2_spawns = 0
                        player.y = ground_y - 40
                        player.height = 40
                        player.width = 40
                        player_velocity_y = 0
                        jump_count = 0

                        c1.x = get_x(screen_rect.width + random.randint(0, 1200), [])
                        obstacles = [c1]
                        c2.x = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
                        obstacles.append(c2)
                        tc1.x = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
                        obstacles.append(tc1)
                        tc2.x = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
                        obstacles.append(tc2)
                        pt.x = get_x(screen_rect.width + random.randint(0, 1200), obstacles)
                        obstacles.append(pt)

                        pt.y = random.choice(pt_spawn_height)
                        current_screen = "playing"
                    elif menu_button.collidepoint(event.pos):
                        return "back"

        screen.fill("black")

        pygame.draw.rect(screen, "white", ground)
        pygame.draw.rect(screen, player_color, player)
        pygame.draw.rect(screen, c1_color, c1)
        pygame.draw.rect(screen, c2_color, c2)

        if true_score >= 500 and pt_spawns > 2:
            pygame.draw.rect(screen, pt_color, pt)

        if true_score >= 500 and tc1_spawns > 2:
            pygame.draw.rect(screen, tc1_color, tc1)

        if true_score >= 500 and tc2_spawns > 2:
            pygame.draw.rect(screen, tc2_color, tc2)

        display_score = true_score // 100

        score_text = text_font.render(f"{display_score}", True, score_color)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (score_title_text_rect.right + 10, 50)

        screen.blit(score_title_text, score_title_text_rect)
        screen.blit(score_text, score_text_rect)

        if current_screen == "playing":
            true_score += 1
            current_speed = 8 + (true_score // 800)

            if keys[pygame.K_DOWN] and player.y >= ground_y - 40:
                player.y = ground_y - 20
                player.height = 20
                player.width = 55
            else:
                if player.y >= ground_y - 40:
                    player.height = 40
                    player.width = 40
                    player.y = ground_y - 40

            if player.y < ground_y - 40 and keys[pygame.K_DOWN]:
                player_velocity_y += 3

            if player.y < ground_y - 40 or player_velocity_y != 0:
                player_velocity_y += gravity
                player.y += player_velocity_y

                if player.y >= ground_y - 40:
                    player.y = ground_y - 40
                    player_velocity_y = 0
                    jump_count = 0

            c1.x -= current_speed

            if c1.right < player.left and not c1_cleared:
                true_score += 50
                c1_cleared = True

            if c1.right < 0:
                other_obstacles = [c2, tc1, tc2, pt]
                c1.x = get_x(screen_rect.width + random.randint(0, 600), other_obstacles)
                c1_cleared = False

                new_height = random.randint(40, 70)
                c1.height = new_height
                c1.y = ground_y - new_height

            c2.x -= current_speed

            if c2.right < player.left and not c2_cleared:
                true_score += 50
                c2_cleared = True

            if c2.right < 0:
                other_obstacles = [c1, tc1, tc2, pt]
                c2.x = get_x(screen_rect.width + random.randint(0, 600), other_obstacles)
                c2_cleared = False

                new_height = random.randint(40, 70)
                c2.height = new_height
                c2.y = ground_y - new_height

            tc1.x -= current_speed

            if tc1.right < player.left and not tc1_cleared:
                if tc1_spawns > 2:
                    true_score += 50
                tc1_cleared = True

            if tc1.right < 0:
                other_obstacles = [c1, c2, tc2, pt]
                tc1.x = get_x(screen_rect.width + random.randint(0, 600), other_obstacles)
                tc1_cleared = False
                tc1_spawns += 1

                new_height = random.randint(75, 95)
                tc1.height = new_height
                tc1.y = ground_y - new_height

            if true_score >= 1200:
                tc2.x -= current_speed

                if tc2.right < player.left and not tc2_cleared:
                    if tc2_spawns > 2:
                        true_score += 50
                    tc2_cleared = True

                if tc2.right < 0:
                    other_obstacles = [c1, c2, tc1, pt]
                    tc2.x = get_x(screen_rect.width + random.randint(0, 600), other_obstacles)
                    tc2_cleared = False
                    tc2_spawns += 1

                    new_height = random.randint(75, 95)
                    tc2.height = new_height
                    tc2.y = ground_y - new_height

            if true_score >= 2200:
                pt.x -= current_speed

                if pt.right < player.left and not pt_cleared:
                    if pt_spawns > 2:
                        true_score += 50
                    pt_cleared = True

                if pt.right < 0:
                    other_obstacles = [c1, c2, tc1, tc2]
                    pt.x = get_x(screen_rect.width + random.randint(0, 600), other_obstacles)
                    pt.y = random.choice(pt_spawn_height)
                    pt_cleared = False
                    pt_spawns += 1

            if player.colliderect(c1):
                current_screen = "game over"

            if player.colliderect(c2):
                current_screen = "game over"

            if tc1_spawns > 2 and player.colliderect(tc1):
                current_screen = "game over"

            if true_score >= 1200 and tc2_spawns > 2 and player.colliderect(tc2):
                current_screen = "game over"

            if true_score >= 2200 and pt_spawns > 2 and player.colliderect(pt):
                current_screen = "game over"

        elif current_screen == "game over":
            game_over_surface = title_font.render("Game Over", True, "white")
            screen.blit(game_over_surface, (center_x - game_over_surface.get_width() // 2, 200))

            pygame.draw.rect(screen, replay_color, replay_button)
            pygame.draw.rect(screen, menu_color, menu_button)

            screen.blit(replay_text, replay_text_rect)
            screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)

    return "back"