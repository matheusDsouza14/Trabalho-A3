import pygame
from config import *


class SistemaUI:

    def __init__(self):

        self.ansiedade_visual = 10

    def atualizar(self, ansiedade_real, dt):

        velocidade_suavizacao = 5

        self.ansiedade_visual += (
            ansiedade_real
            - self.ansiedade_visual
        ) * velocidade_suavizacao * dt

        self.ansiedade_visual = max(
            0,
            min(100, self.ansiedade_visual)
        )

    def desenhar(self, tela, fonte):

        pygame.draw.rect(
            tela,
            FUNDO,
            (15, 10, 450, 120)
        )

        texto = fonte.render(
            f"Ansiedade: {int(self.ansiedade_visual)}%",
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (40, 25)
        )

        rect_fundo = pygame.Rect(
            40,
            70,
            360,
            30
        )

        painel = pygame.Surface(
            (360, 30),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            painel,
            (22, 22, 32),
            (0, 0, 360, 30),
            border_radius=14
        )

        tela.blit(
            painel,
            (40, 70)
        )

        largura_preenchimento = int(
            (self.ansiedade_visual / 100)
            * 360
        )

        rect_preenchimento = pygame.Rect(
            40,
            70,
            largura_preenchimento,
            30
        )

        if self.ansiedade_visual < 35:
            cor = (100, 200, 255)

        elif self.ansiedade_visual < 70:
            cor = (255, 210, 90)

        else:
            cor = (255, 90, 90)

        pygame.draw.rect(
            tela,
            cor,
            rect_preenchimento,
            border_radius=14
        )

        pygame.draw.rect(
            tela,
            BRANCO,
            rect_fundo,
            2,
            border_radius=14
        )