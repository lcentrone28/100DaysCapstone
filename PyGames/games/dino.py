import pygame
import PyGames.pause as pause

def run_dino(screen, clock):
    running = True
    is_paused = False

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

        pygame.display.flip()
        clock.tick(60)

    return "back"