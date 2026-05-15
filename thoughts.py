import pygame
import random

from config import *

# =========================================================
# PENSAMENTOS NEGATIVOS
# =========================================================

PENSAMENTOS_NEGATIVOS = [

    "Todos perceberam seu nervosismo",
    "Você vai perder o controle",
    "Estão julgando você",
    "Sua voz está tremendo",
    "Você vai falhar",
    "Você parece estranho",
    "Todos estão olhando",
    "Você vai esquecer tudo"

]

# =========================================================
# PENSAMENTOS POSITIVOS
# =========================================================

PENSAMENTOS_POSITIVOS = [

    "Continue respirando",
    "Você consegue",
    "Vai ficar tudo bem",
    "Continue falando",
    "Respire devagar",
    "Você está no controle",
    "Ninguém percebeu",
    "Você está indo bem",
    "Só continue",
    "Foque na apresentação",
    "Você consegue passar por isso",
    "Continue calmo",
    "Respire profundamente",
    "Você ainda está conseguindo"

]

# =========================================================
# PENSAMENTO
# =========================================================

class Pensamento:

    def __init__(self, texto, positivo):

        self.texto = texto

        self.positivo = positivo

        self.clicado = False

        self.fonte = pygame.font.Font(
            FONTE,
            int(30 * 1.07)
        )

        largura_texto = self.fonte.size(
            texto
        )[0]

        self.largura = max(
            320,
            largura_texto + 60
        )

        self.altura = 120

        # =================================================
        # POSITIVOS SOMEM
        # NEGATIVOS FICAM
        # =================================================

        self.tempo = 30 if positivo else -1

        # =================================================
        # POSIÇÃO
        # =================================================

        while True:

            self.x = random.randint(100, 780)

            self.y = random.randint(80, 520)

            # NÃO SOBREPOR RESPIRAÇÃO

            if not (
                self.x > 850 and
                self.y > 450
            ):
                break

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def atualizar(self, dt):

        if self.positivo:

            self.tempo -= dt

    # =====================================================
    # DRAW
    # =====================================================

    def desenhar(self, tela):

        if self.positivo:

            fundo = (40, 90, 60)

            borda = VERDE

        else:

            fundo = (90, 40, 40)

            borda = VERMELHO

        pygame.draw.rect(
            tela,
            fundo,
            self.rect,
            border_radius=18
        )

        pygame.draw.rect(
            tela,
            borda,
            self.rect,
            4,
            border_radius=18
        )

        render = self.fonte.render(
            self.texto,
            True,
            BRANCO
        )

        tela.blit(
            render,
            (
                self.rect.centerx
                - render.get_width() // 2,

                self.rect.centery
                - render.get_height() // 2
            )
        )

# =========================================================
# SISTEMA DE PENSAMENTOS
# =========================================================

class SistemaPensamentos:

    def __init__(self):

        self.pensamentos = []

        self.temporizador_spawn = 0

        # =================================================
        # CHANCE BASE
        # =================================================

        self.chance_negativa = 0.12

    # =====================================================
    # CRIAR PENSAMENTO
    # =====================================================

    def criar_pensamento(self, positivo):

        lista = (
            PENSAMENTOS_POSITIVOS
            if positivo
            else PENSAMENTOS_NEGATIVOS
        )

        return Pensamento(
            random.choice(lista),
            positivo
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def atualizar(self, eventos, estado_jogo, dt):

        self.temporizador_spawn += dt

        mudanca_ansiedade = 0

        clique_consumido = False

        # =================================================
        # VELOCIDADE DE SPAWN
        # =================================================

        velocidade_spawn = 2.5

        if estado_jogo.ansiedade > 60:

            velocidade_spawn = 1.8

        # =================================================
        # RESPIRAR AUMENTA NEGATIVOS
        # =================================================

        if estado_jogo.respiracao.segurar:

            chance_negativa_atual = 0.45

        else:

            chance_negativa_atual = self.chance_negativa

        # =================================================
        # GERAR PENSAMENTOS
        # =================================================

        if self.temporizador_spawn >= velocidade_spawn:

            self.temporizador_spawn = 0

            positivo = (
                random.random()
                > chance_negativa_atual
            )

            pensamento = self.criar_pensamento(
                positivo
            )

            self.pensamentos.append(
                pensamento
            )

            # =============================================
            # NEGATIVOS AUMENTAM PRESSÃO
            # =============================================

            if not positivo:

                estado_jogo.velocidade_ansiedade += 1

        # =================================================
        # CLIQUES
        # =================================================

        for evento in eventos:

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    for pensamento in reversed(
                        self.pensamentos
                    ):

                        if pensamento.rect.collidepoint(
                            evento.pos
                        ):

                            clique_consumido = True

                            pensamento.clicado = True

                            # =================================
                            # POSITIVOS AJUDAM
                            # =================================

                            if pensamento.positivo:

                                mudanca_ansiedade -= 18

                            break

        # =================================================
        # UPDATE PENSAMENTOS
        # =================================================

        for pensamento in self.pensamentos:

            pensamento.atualizar(dt)

            if pensamento.positivo:

                if pensamento.tempo <= 0:

                    pensamento.clicado = True

        # =================================================
        # REMOVER
        # =================================================

        self.pensamentos = [

            pensamento

            for pensamento in self.pensamentos

            if not pensamento.clicado
        ]

        return mudanca_ansiedade, clique_consumido

    # =====================================================
    # DRAW
    # =====================================================

    def desenhar(self, tela):

        for pensamento in self.pensamentos:

            pensamento.desenhar(tela)