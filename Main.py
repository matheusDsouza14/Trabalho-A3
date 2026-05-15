import pygame
import sys

from config import *
from game_state import GameState
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Hold Your Breath")

    clock = pygame.time.Clock()

    game = GameState(screen)

    while game.running:

        dt = clock.tick(FPS) / 1000

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update(dt, events)

        game.draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()