import pygame
import pause
from colors import colors, text_color
import random
import json

WIN_CONDITIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner(board):
    for condition in WIN_CONDITIONS:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != "":
            return board[condition[0]]
    return None

def computer_move(board, computer_symbol):
    player_symbol = "O" if computer_symbol == "X" else "X"

    for condition in WIN_CONDITIONS:
        values = [board[condition[0]], board[condition[1]], board[condition[2]]]
        if values.count(computer_symbol) == 2 and values.count("") == 1:
            return condition[values.index("")]

    for condition in WIN_CONDITIONS:
        values = [board[condition[0]], board[condition[1]], board[condition[2]]]
        if values.count(player_symbol) == 2 and values.count("") == 1:
            return condition[values.index("")]

    empty_cells = [index for index, value in enumerate(board) if value == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None

def run_ttt(screen, clock):
    running = True
    stats_updated = False

    current_screen = "mode select"
    game_mode = None
    player_role = ""
    current_turn = None
    board = [""] * 9
    game_result = None

    computer_timer = 0
    computer_delay_active = False

    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    button_font = pygame.font.SysFont("Arial", 30)

    screen_rect = screen.get_rect()
    cell_size = 120
    grid_start_x = screen_rect.centerx - (cell_size * 1.5)
    grid_start_y = screen_rect.centery - (cell_size * 1.5)
    center_x = screen_rect.centerx

    single_color = random.choice(colors)
    multiplayer_color = random.choice(colors)
    replay_color = random.choice(colors)
    menu_color = random.choice(colors)
    x_color = random.choice(colors)
    o_color = random.choice(colors)

    single_text_color = text_color(single_color)
    multiplayer_text_color = text_color(multiplayer_color)
    replay_text_color = text_color(replay_color)
    menu_text_color = text_color(menu_color)

    single_button = pygame.Rect(0, 0, 270, 50)
    multiplayer_button = pygame.Rect(0, 0, 270, 50)

    single_button.centerx = center_x
    multiplayer_button.centerx = center_x

    single_button.y = 320
    multiplayer_button.y = 400

    single_text = button_font.render("The Computer", True, single_text_color)
    single_text_rect = single_text.get_rect()
    single_text_rect.center = single_button.center

    multiplayer_text = button_font.render("Another Player", True, multiplayer_text_color)
    multiplayer_text_rect = multiplayer_text.get_rect()
    multiplayer_text_rect.center = multiplayer_button.center

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

        screen.fill("black")

        if current_screen == "mode select":
            title_surface = title_font.render("Who would you like to play against?", True, "white")
            screen.blit(title_surface, (center_x - title_surface.get_width() // 2, 200))

            pygame.draw.rect(screen, single_color, single_button)
            pygame.draw.rect(screen, multiplayer_color, multiplayer_button)

            screen.blit(single_text, single_text_rect)
            screen.blit(multiplayer_text, multiplayer_text_rect)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if single_button.collidepoint(event.pos):
                        game_mode = "single"
                        board = [""] * 9
                        player_role = random.choice(["X", "O"])
                        current_turn = random.choice(["X", "O"])
                        computer_delay_active = False
                        current_screen = "playing"
                    elif multiplayer_button.collidepoint(event.pos):
                        game_mode = "multiplayer"
                        board = [""] * 9
                        current_turn = random.choice(["X", "O"])
                        current_screen = "playing"

        elif current_screen == "playing":
            if game_mode == "single":
                if current_turn == player_role:
                    turn_text = "Player's Turn"
                else:
                    turn_text = "Computer's Turn"
            else:
                if current_turn == "X":
                    turn_text = "Player 1's Turn"
                else:
                    turn_text = "Player 2's Turn"

            turn_surface = title_font.render(turn_text, True, "white")
            screen.blit(turn_surface, (center_x - turn_surface.get_width() // 2, 100))

            cells = []

            for row in range(3):
                for col in range(3):
                    x = grid_start_x + col * cell_size
                    y = grid_start_y + row * cell_size
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    cells.append(rect)

                    pygame.draw.rect(screen, "white", rect, 2)
                    board_index = row * 3 + col
                    if board[board_index] != "":
                        move_surface = title_font.render(board[board_index], True,
                                                         x_color if board[board_index] == "X" else o_color)
                        screen.blit(move_surface, (rect.centerx - move_surface.get_width() // 2,
                                                   rect.centery - move_surface.get_height() // 2))

            if game_mode == "single" and current_turn != player_role:
                if not computer_delay_active:
                    computer_timer = pygame.time.get_ticks()
                    computer_delay_active = True

                if pygame.time.get_ticks() - computer_timer >= random.randint(500, 800):
                    chosen_index = computer_move(board, current_turn)
                    if chosen_index is not None:
                        board[chosen_index] = current_turn

                        winner = check_winner(board)
                        if winner:
                            game_result = f"{winner} Wins"
                            current_screen = "game over"
                        elif "" not in board:
                            game_result = "It's a Tie"
                            current_screen = "game over"
                        else:
                            current_turn = player_role
                    computer_delay_active = False

            else:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for i, rect in enumerate(cells):
                            if rect.collidepoint(event.pos) and board[i] == "":
                                board[i] = current_turn

                                winner = check_winner(board)
                                if winner:
                                    game_result = f"{winner} Wins!"
                                    current_screen = "game over"
                                elif "" not in board:
                                    game_result = "It's a Tie"
                                    current_screen = "game over"
                                else:
                                    current_turn = "O" if current_turn == "X" else "X"
        if current_screen == "game over" and not stats_updated:
            try:
                with open("stats.json", "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {
                    "tic_tac_toe": {
                        "single_player": {"wins": 0, "losses": 0, "ties": 0},
                        "multiplayer": {"wins": 0, "losses": 0, "ties": 0}
                    }
                }

            mode_key = "single_player" if game_mode == "single" else "multiplayer"

            if "Tie" in game_result:
                data["tic_tac_toe"][mode_key]["ties"] += 1
            elif game_mode == "single":
                if player_role in game_result:
                    data["tic_tac_toe"][mode_key]["wins"] += 1
                else:
                    data["tic_tac_toe"][mode_key]["losses"] += 1
            else:
                if "X" in game_result:
                    data["tic_tac_toe"][mode_key]["wins"] += 1
                else:
                    data["tic_tac_toe"][mode_key]["losses"] += 1

            with open("stats.json", "w") as file:
                json.dump(data, file, indent=4)

            stats_updated = True

        elif current_screen == "game over":

            if game_result == "It's a Tie":
                result_surface = title_font.render(game_result, True, "white")
            else:
                result_surface = title_font.render(game_result, True, random.choice(colors))

            screen.blit(result_surface, (center_x - result_surface.get_width() // 2, 200))

            pygame.draw.rect(screen, replay_color, replay_button)
            pygame.draw.rect(screen, menu_color, menu_button)

            screen.blit(replay_text, replay_text_rect)
            screen.blit(menu_text, menu_text_rect)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if replay_button.collidepoint(event.pos):
                        stats_updated = False
                        current_screen = "mode select"
                    elif menu_button.collidepoint(event.pos):
                        return "back"

        pygame.display.flip()
        clock.tick(60)

    return "back"