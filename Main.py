import pygame
import sys

from config import *
from game_state import EstadoJogo


def main():

    pygame.init()

    tela = pygame.display.set_mode(
        (LARGURA, ALTURA)
    )

    pygame.display.set_caption(
        "Segure Sua Respiração"
    )

    relogio = pygame.time.Clock()

    jogo = EstadoJogo(tela)

    while jogo.rodando:

        dt = relogio.tick(FPS) / 1000

        eventos = pygame.event.get()

        for evento in eventos:

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

        jogo.atualizar(dt, eventos)

        jogo.desenhar()

        pygame.display.flip()


if __name__ == "__main__":
    main()