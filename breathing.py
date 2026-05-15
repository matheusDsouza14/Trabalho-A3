import pygame
import math
from config import *


class SistemaRespiracao:
    def __init__(self):
        self.raio_base = 55
        self.raio = self.raio_base
        self.raio_maximo = 75

        self.segurar = False
        self.tempo_segurando = 0
        self.completado = False

        self.centro = (
            LARGURA - 120,
            ALTURA - 120
        )

        self.fonte = pygame.font.Font(
            FONTE,
            int(22 * 1.07)
        )

        self.temporizador_animacao = 0

    def atualizar(self, eventos, dt):
        mouse = pygame.mouse.get_pos()

        self.completado = False
        self.temporizador_animacao += dt

        distancia = math.dist(
            mouse,
            self.centro
        )

        passando_mouse = distancia <= self.raio

        mouse_pressionado = pygame.mouse.get_pressed()[0]

        if passando_mouse and mouse_pressionado:
            self.segurar = True
            self.tempo_segurando += dt

            pulso = math.sin(
                self.temporizador_animacao * 4
            ) * 8

            self.raio = self.raio_base + pulso

            if self.tempo_segurando >= 2:
                self.completado = True
                self.tempo_segurando = 0

        else:
            self.segurar = False
            self.tempo_segurando = 0

            self.raio += (
                self.raio_base - self.raio
            ) * 0.15

        return self.completado

    def desenhar(self, tela):

        brilho = pygame.Surface(
            (220, 220),
            pygame.SRCALPHA
        )

        raio_brilho = int(self.raio + 18)

        pygame.draw.circle(
            brilho,
            (120, 180, 255, 40),
            (110, 110),
            raio_brilho
        )

        tela.blit(
            brilho,
            (
                self.centro[0] - 110,
                self.centro[1] - 110
            )
        )

        cor = (120, 170, 255)

        if self.segurar:
            cor = (170, 210, 255)

        pygame.draw.circle(
            tela,
            cor,
            self.centro,
            int(self.raio)
        )

        pygame.draw.circle(
            tela,
            BRANCO,
            self.centro,
            int(self.raio),
            4
        )

        texto = "Respire..." if self.segurar else "Segure"

        render = self.fonte.render(
            texto,
            True,
            BRANCO
        )

        tela.blit(
            render,
            (
                self.centro[0] - render.get_width() // 2,
                self.centro[1] - render.get_height() // 2
            )
        )

        progresso = min(
            self.tempo_segurando / 2,
            1
        )

        largura_barra = 120

        rect_barra = pygame.Rect(
            self.centro[0] - 60,
            self.centro[1] + 85,
            largura_barra,
            10
        )

        pygame.draw.rect(
            tela,
            (40, 40, 50),
            rect_barra,
            border_radius=8
        )

        pygame.draw.rect(
            tela,
            (120, 200, 255),
            (
                rect_barra.x,
                rect_barra.y,
                largura_barra * progresso,
                10
            ),
            border_radius=8
        )