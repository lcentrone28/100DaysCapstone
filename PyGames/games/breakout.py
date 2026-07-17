import pygame
import PyGames.pause as pause
from colors import colors, text_color
import random
import json

def init_blocks(rows, cols, x_start, y_start, w, h, x_space, y_space,
                brick_colors):
    blocks_list = []
    for row in range(rows):
        for col in range(cols):
            ax = x_start + col * (w + x_space)
            ay = y_start + row * (h + y_space)

            if row in [0, 1]:
                tier = 7
            elif row in [2, 3]:
                tier = 5
            elif row in [4, 5]:
                tier = 3
            else:
                tier = 1

            color = brick_colors[(row // 2) % len(brick_colors)]

            blocks_list.append({
                'rect': pygame.Rect(ax, ay, w, h),
                'tier_score': tier,
                'is_cavity': False,
                'color': color
            })
    return blocks_list

def run_breakout(screen, clock):
    running = True
    stats_updated = False

    current_screen = "mode select"
    game_mode = None
    cavity_mode = False

    score = 0
    balls_left = 0
    active_balls = 0

    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    button_font = pygame.font.SysFont("Arial", 30)

    screen_rect = screen.get_rect()
    center_x = screen_rect.centerx

    replay_color = random.choice(colors)
    menu_color = random.choice(colors)

    replay_text_color = text_color(replay_color)
    menu_text_color = text_color(menu_color)

    get_colors = random.sample(colors, 16)

    assign_colors = {
        'player1': get_colors[0],
        'player2': get_colors[1],
        'brick1': get_colors[2],
        'brick2': get_colors[3],
        'brick3': get_colors[4],
        'brick4': get_colors[5],
        'ball1': get_colors[6],
        'ball2': get_colors[7],
        'ball3': get_colors[8],
        'ball4': get_colors[9],
        'ball5': get_colors[10],
        'score_title': get_colors[11],
        'score_text': get_colors[12],
        'balls_left_title': get_colors[13],
        'balls_left_text': get_colors[14],
        'cavity_toggle': get_colors[15],
    }

    p1_color = assign_colors['player1']
    p2_color = assign_colors['player2']
    br1_color = assign_colors['brick1']
    br2_color = assign_colors['brick2']
    br3_color = assign_colors['brick3']
    br4_color = assign_colors['brick4']
    b1_color = assign_colors['ball1']
    b2_color = assign_colors['ball2']
    b3_color = assign_colors['ball3']
    b4_color = assign_colors['ball4']
    b5_color = assign_colors['ball5']
    score_title_color = assign_colors['score_title']
    score_color = assign_colors['score_text']
    balls_left_title_color = assign_colors['balls_left_title']
    balls_left_color = assign_colors['balls_left_text']
    cavity_toggle_color = assign_colors['cavity_toggle']

    ball_colors = [b1_color, b2_color, b3_color, b4_color, b5_color]
    brick_colors = [br1_color, br2_color, br3_color, br4_color]

    p1_text_color = text_color(p1_color)
    p2_text_color = text_color(p2_color)
    cavity_toggle_text_color = text_color(cavity_toggle_color)

    player_width = 100
    player_height = 20
    player_speed = 15

    rows = 8
    columns = 14

    blocks_h = 25
    x_spacing = 8
    y_spacing = 8
    margin = 20

    blocks = []

    balls = []
    ball_speed = 6
    ball_size = 15

    player1 = pygame.Rect(0, screen_rect.height - 70, player_width, player_height)
    player2 = pygame.Rect(0, screen_rect.height - 70, player_width, player_height)

    width = screen_rect.width - (margin * 2) - (x_spacing * (columns - 1))
    blocks_w = width // columns
    grid_start_x = (screen_rect.width - (columns * blocks_w + (columns - 1) * x_spacing)) // 2

    p1_button = pygame.Rect(0, 0, 270, 50)
    p2_button = pygame.Rect(0, 0, 270, 50)

    p1_button.centerx = center_x
    p2_button.centerx = center_x

    p1_button.y = 220
    p2_button.y = 290

    cavity_toggle_button = pygame.Rect(0, 0, 270, 50)
    cavity_toggle_button.centerx = center_x
    cavity_toggle_button.y = 380

    title_surface = title_font.render("Select Breakout Mode", True, "white")
    screen.blit(title_surface, (center_x - title_surface.get_width() // 2, 120))

    p1_text = button_font.render("Single Player", True, p1_text_color)
    p1_text_rect = p1_text.get_rect()
    p1_text_rect.center = p1_button.center

    p2_text = button_font.render("Multiplayer", True, p2_text_color)
    p2_text_rect = p2_text.get_rect()
    p2_text_rect.center = p2_button.center

    toggle_label = "Cavity Mode: ON" if cavity_mode else "Cavity Mode: OFF"
    toggle_text = button_font.render(toggle_label, True, cavity_toggle_text_color)
    toggle_text_rect = toggle_text.get_rect()

    score_title_text = button_font.render("Score: ", True, score_title_color)
    score_value_text = button_font.render(f"{score}", True, score_color)

    balls_left_title_text = button_font.render("Balls Left: ", True, balls_left_title_color)
    balls_left_text = button_font.render(f"{balls_left}", True, balls_left_color)

    s_title_w = score_title_text.get_width()
    s_val_w = score_value_text.get_width()
    b_title_w = balls_left_title_text.get_width()
    b_val_w = balls_left_text.get_width()

    total_hud_width = s_title_w + s_val_w + 40 + b_title_w + b_val_w
    start_x = center_x - total_hud_width // 2
    hud_y = screen_rect.height - 45

    balls_start_x = start_x + s_title_w + s_val_w + 40

    replay_button = pygame.Rect(0, 0, 350, 50)
    menu_button = pygame.Rect(0, 0, 350, 50)

    replay_button.centerx = center_x
    menu_button.centerx = center_x
    replay_button.y = 320
    menu_button.y = 400

    replay_text = button_font.render("Replay?", True, replay_text_color)
    replay_text_rect = replay_text.get_rect()
    replay_text_rect.center = replay_button.center

    menu_text = button_font.render("Back to Main Menu", True, menu_text_color)
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

            if current_screen == "mode select":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_mode = None

                    if p1_button.collidepoint(event.pos):
                        game_mode = "single"
                    elif p2_button.collidepoint(event.pos):
                        game_mode = "multiplayer"
                    elif cavity_toggle_button.collidepoint(event.pos):
                        cavity_mode = not cavity_mode

                        toggle_label = "Cavity Mode: ON" if cavity_mode else "Cavity Mode: OFF"
                        toggle_text = button_font.render(toggle_label, True, cavity_toggle_text_color)
                        toggle_text_rect = toggle_text.get_rect()
                        toggle_text_rect.center = cavity_toggle_button.center

                    if game_mode:
                        score = 0
                        balls_left = 10 if game_mode == "multiplayer" else 5

                        score_value_text = button_font.render(f"{score}", True, score_color)
                        balls_left_text = button_font.render(f"{balls_left}", True, balls_left_color)

                        grid_start_y = 40

                        blocks.clear()
                        blocks.extend(
                            init_blocks(rows, columns, grid_start_x, grid_start_y, blocks_w, blocks_h, x_spacing,
                                        y_spacing, brick_colors))

                        if cavity_mode:
                            for row_index in range(rows):
                                row_blocks = blocks[row_index * columns:(row_index + 1) * columns]

                                if len(row_blocks) > 0:
                                    random.choice(row_blocks)['is_cavity'] = True

                        balls.clear()

                        if game_mode == "multiplayer":
                            player1.centerx = center_x - 150
                            player2.centerx = center_x + 150

                            active_balls = 2

                            balls.append({
                                'rect': pygame.Rect(player1.centerx - ball_size // 2, player1.top - ball_size,
                                                    ball_size, ball_size),
                                'x': float(player1.centerx - ball_size // 2),
                                'y': float(player1.top - ball_size),
                                'dx': float(-ball_speed // 2),
                                'dy': float(-ball_speed),
                                'color': random.choice(ball_colors),
                                'has_hit_paddle': False
                            })

                            balls.append({
                                'rect': pygame.Rect(player2.centerx - ball_size // 2, player2.top - ball_size,
                                                    ball_size, ball_size),
                                'x': float(player2.centerx - ball_size // 2),
                                'y': float(player2.top - ball_size),
                                'dx': float(ball_speed // 2),
                                'dy': float(-ball_speed),
                                'color': random.choice(ball_colors),
                                'has_hit_paddle': False
                            })
                        else:
                            player1.centerx = center_x

                            active_balls = 1

                            balls.append({
                                'rect': pygame.Rect(center_x - ball_size // 2, screen_rect.height - 150, ball_size,
                                                    ball_size),
                                'x': float(center_x - ball_size // 2),
                                'y': float(screen_rect.height - 150),
                                'dx': float(ball_speed),
                                'dy': float(-ball_speed),
                                'color': random.choice(ball_colors),
                                'has_hit_paddle': False
                            })

                        current_screen = "playing"

            elif current_screen in ["game over", "game won"]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if replay_button.collidepoint(event.pos):
                        stats_updated = False
                        game_mode = None

                        score = 0
                        balls_left = 0
                        active_balls = 0
                        current_screen = "mode select"
                    elif menu_button.collidepoint(event.pos):
                        return "back"

        if current_screen == "playing":
            keys = pygame.key.get_pressed()

            speed_factor = 1.0 + (score / 400.0)
            current_paddle_speed = int(player_speed * speed_factor)

            if game_mode == "multiplayer":
                if keys[pygame.K_a]:
                    player1.x -= current_paddle_speed
                if keys[pygame.K_d]:
                    player1.x += current_paddle_speed

                if keys[pygame.K_LEFT]:
                    player2.x -= current_paddle_speed
                if keys[pygame.K_RIGHT]:
                    player2.x += current_paddle_speed
            else:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player1.x -= current_paddle_speed
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player1.x += current_paddle_speed

            if player1.left < 0: player1.left = 0
            if player1.right > screen_rect.width: player1.right = screen_rect.width

            if player2.left < 0: player2.left = 0
            if player2.right > screen_rect.width: player2.right = screen_rect.width

            for b in balls[:]:
                ball_rect = b['rect']
                old_x, old_y = ball_rect.x, ball_rect.y

                speed_mod = 0.8 if not b['has_hit_paddle'] else 1.0

                b['x'] += b['dx'] * speed_factor * speed_mod
                b['y'] += b['dy'] * speed_factor * speed_mod
                ball_rect.x = int(b['x'])
                ball_rect.y = int(b['y'])

                if ball_rect.left <= 0:
                    ball_rect.left = 0
                    b['x'] = 0.0
                    b['dx'] *= -1
                elif ball_rect.right >= screen_rect.width:
                    ball_rect.right = screen_rect.width
                    b['x'] = float(screen_rect.width - ball_rect.width)
                    b['dx'] *= -1

                if ball_rect.top <= 40:
                    ball_rect.top = 40
                    b['y'] = 40.0
                    b['dy'] *= -1

                if ball_rect.top >= screen_rect.height:
                    balls.remove(b)
                    active_balls -= 1
                    continue

                if ball_rect.colliderect(player1) and b['dy'] > 0:
                    ball_rect.bottom = player1.top
                    b['y'] = float(player1.top - ball_rect.height)
                    b['dy'] *= -1
                    relative_intersect = (player1.centerx - ball_rect.centerx) / (player1.width / 2)
                    b['dx'] = float(-relative_intersect * ball_speed)
                    b['has_hit_paddle'] = True

                if game_mode == "multiplayer":
                    if ball_rect.colliderect(player2) and b['dy'] > 0:
                        ball_rect.bottom = player2.top
                        b['y'] = float(player2.top - ball_rect.height)
                        b['dy'] *= -1
                        relative_intersect = (player2.centerx - ball_rect.centerx) / (player2.width / 2)
                        b['dx'] = float(-relative_intersect * ball_speed)
                        b['has_hit_paddle'] = True

                for b_dict in blocks[:]:
                    brick = b_dict['rect']

                    if ball_rect.colliderect(brick):
                        if old_x + ball_rect.width <= brick.left or old_x >= brick.right:
                            b['dx'] *= -1
                        else:
                            b['dy'] *= -1

                        if cavity_mode and b_dict['is_cavity']:
                            rand_dir = random.choice([-1, 1])
                            balls.append({
                                'rect': pygame.Rect(brick.centerx, brick.centery, ball_size, ball_size),
                                'x': float(brick.centerx),
                                'y': float(brick.centery),
                                'dx': float(ball_speed * rand_dir),
                                'dy': float(ball_speed),
                                'color': random.choice(ball_colors),
                                'has_hit_paddle': False
                            })
                            active_balls += 1

                        score += b_dict['tier_score']
                        score_value_text = button_font.render(f"{score}", True, score_color)
                        blocks.remove(b_dict)
                        break

            if active_balls <= 0:
                balls_left -= 1
                balls_left_text = button_font.render(f"{balls_left}", True, balls_left_color)

                if balls_left <= 0:
                    current_screen = "game over"
                else:
                    if game_mode == "multiplayer":
                        player1.centerx = center_x - 150
                        player2.centerx = center_x + 150

                        active_balls = 2

                        balls.append({
                            'rect': pygame.Rect(player1.centerx - ball_size // 2, player1.top - ball_size, ball_size,
                                                ball_size),
                            'x': float(player1.centerx - ball_size // 2),
                            'y': float(player1.top - ball_size),
                            'dx': float(-ball_speed // 2),
                            'dy': float(-ball_speed),
                            'color': random.choice(ball_colors),
                            'has_hit_paddle': False
                        })

                        balls.append({
                            'rect': pygame.Rect(player2.centerx - ball_size // 2, player2.top - ball_size, ball_size,
                                                ball_size),
                            'x': float(player2.centerx - ball_size // 2),
                            'y': float(player2.top - ball_size),
                            'dx': float(ball_speed // 2),
                            'dy': float(-ball_speed),
                            'color': random.choice(ball_colors),
                            'has_hit_paddle': False
                        })
                    else:
                        player1.centerx = center_x

                        active_balls = 1

                        balls.append({
                            'rect': pygame.Rect(center_x - ball_size // 2, screen_rect.height - 150, ball_size,
                                                ball_size),
                            'x': float(center_x - ball_size // 2),
                            'y': float(screen_rect.height - 150),
                            'dx': float(ball_speed * random.choice([-1, 1])),
                            'dy': float(-ball_speed),
                            'color': random.choice(ball_colors),
                            'has_hit_paddle': False
                        })

            if len(blocks) == 0:
                current_screen = "game won"

        screen.fill("black")

        if current_screen == "mode select":
            pygame.draw.rect(screen, p1_color, p1_button)
            screen.blit(p1_text, p1_text_rect)

            pygame.draw.rect(screen, p2_color, p2_button)
            screen.blit(p2_text, p2_text_rect)

            pygame.draw.rect(screen, cavity_toggle_color, cavity_toggle_button)
            toggle_text_rect.center = cavity_toggle_button.center
            screen.blit(toggle_text, toggle_text_rect)

        elif current_screen == "playing":
            for b_dict in blocks:
                brick = b_dict['rect']
                pygame.draw.rect(screen, b_dict['color'], brick)

                if cavity_mode and b_dict['is_cavity']:
                    pygame.draw.rect(screen, "white", brick, 2)

            pygame.draw.rect(screen, p1_color, player1)

            if game_mode == "multiplayer":
                pygame.draw.rect(screen, p2_color, player2)

            for b in balls:
                pygame.draw.ellipse(screen, b['color'], b['rect'])

            screen.blit(score_title_text, (start_x, hud_y))
            screen.blit(score_value_text, (start_x + s_title_w, hud_y))

            screen.blit(balls_left_title_text, (balls_start_x, hud_y))
            screen.blit(balls_left_text, (balls_start_x + b_title_w, hud_y))

        if current_screen in ["game over", "game won"] and not stats_updated:
            try:
                with open("stats.json", "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {
                    "breakout": {
                        "single_player": {"cavity_enabled": 0, "cavity_disabled": 0},
                        "multiplayer": {"cavity_enabled": 0, "cavity_disabled": 0}
                    }
                }

            mode_key = "single_player" if game_mode == "single" else "multiplayer"
            cavity_key = "cavity_enabled" if cavity_mode else "cavity_disabled"

            if score > data["breakout"][mode_key][cavity_key]:
                data["breakout"][mode_key][cavity_key] = score
                with open("stats.json", "w") as file:
                    json.dump(data, file, indent=4)
            stats_updated = True

        elif current_screen in ["game over", "game won"]:
            msg = "You Win" if current_screen == "game won" else "Game Over"
            title_surface = title_font.render(msg, True, "white")
            title_x = center_x - title_surface.get_width() // 2
            title_y = 180
            screen.blit(title_surface, (title_x, title_y))

            final_score_text = button_font.render(f"Score: {score}", True, "white")
            score_x = center_x - final_score_text.get_width() // 2
            score_y = title_y + title_surface.get_height() + 10
            screen.blit(final_score_text, (score_x, score_y))

            pygame.draw.rect(screen, replay_color, replay_button)
            pygame.draw.rect(screen, menu_color, menu_button)

            screen.blit(replay_text, replay_text_rect)
            screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)

    return "back"