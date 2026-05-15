import pygame
import random

from config import *

# =========================================================
# BANCO DE PERGUNTAS
# =========================================================

BANCO_PERGUNTAS = [

    {
        "pergunta": "O que pode ajudar a reduzir a ansiedade?",
        "escolhas": [
            "Respirar devagar",
            "Manter o foco",
            "Falar com calma",
            "Continuar apresentando"
        ]
    },

    {
        "pergunta": "Qual é um sintoma comum da ansiedade?",
        "escolhas": [
            "Voz tremendo",
            "Mãos suando",
            "Falta de ar",
            "Pensamentos acelerados"
        ]
    },

    {
        "pergunta": "O que pensamentos negativos podem causar?",
        "escolhas": [
            "Mais ansiedade",
            "Mais medo",
            "Mais insegurança",
            "Pânico"
        ]
    },

    {
        "pergunta": "O que pode ajudar durante uma crise?",
        "escolhas": [
            "Controlar a respiração",
            "Respirar lentamente",
            "Se acalmar",
            "Focar no presente"
        ]
    },

    {
        "pergunta": "O que a ansiedade pode distorcer?",
        "escolhas": [
            "A percepção",
            "Os pensamentos",
            "A confiança",
            "A realidade"
        ]
    },

    {
        "pergunta": "O que pode ajudar alguém ansioso?",
        "escolhas": [
            "Pensamentos positivos",
            "Respiração",
            "Calma",
            "Apoio"
        ]
    },

    {
        "pergunta": "O que ajuda a prevenir ansiedade extrema?",
        "escolhas": [
            "Descansar",
            "Respirar",
            "Dormir bem",
            "Diminuir pressão"
        ]
    },

    {
        "pergunta": "Qual é a principal luta do personagem?",
        "escolhas": [
            "Os próprios pensamentos",
            "O medo",
            "A ansiedade",
            "A pressão"
        ]
    },

    {
        "pergunta": "Qual é a mensagem principal do jogo?",
        "escolhas": [
            "A ansiedade engana sua mente",
            "Você consegue continuar",
            "Nem tudo é real",
            "Você não está sozinho"
        ]
    }

]

# =========================================================
# SISTEMA DE APRESENTAÇÃO
# =========================================================

class SistemaApresentacao:

    def __init__(self, quantidade):

        self.perguntas = random.sample(
            BANCO_PERGUNTAS,
            quantidade
        )

        self.indice = 0

        self.completado = False

        self.fonte = pygame.font.Font(
            FONTE,
            int(36 * 1.07)
        )

        self.fonte_pequena = pygame.font.Font(
            FONTE,
            int(26 * 1.07)
        )

        self.feedback = ""

        self.temporizador_feedback = 0

        self.rects_botoes = []

    # =====================================================
    # PERGUNTA ATUAL
    # =====================================================

    @property
    def pergunta_atual(self):

        return self.perguntas[self.indice]

    # =====================================================
    # BOTÕES RESPONSIVOS
    # =====================================================

    def criar_botao_responsivo(self, texto, y):

        largura_texto = self.fonte_pequena.size(
            texto
        )[0]

        largura = max(
            320,
            largura_texto + 60
        )

        altura = 65

        # =============================================
        # ALINHADO À ESQUERDA
        # =============================================

        x = 70

        return pygame.Rect(
            x,
            y,
            largura,
            altura
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def atualizar(self, eventos, estado_jogo):

        if self.completado:
            return

        mouse = pygame.mouse.get_pos()

        self.rects_botoes.clear()

        for i, escolha in enumerate(
            self.pergunta_atual["escolhas"]
        ):

            rect = self.criar_botao_responsivo(
                escolha,
                240 + i * 95
            )

            self.rects_botoes.append(rect)

        for evento in eventos:

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    for rect in self.rects_botoes:

                        if rect.collidepoint(mouse):

                            # =============================
                            # TODAS AS RESPOSTAS
                            # AVANÇAM A APRESENTAÇÃO
                            # E AUMENTAM ANSIEDADE
                            # =============================

                            self.feedback = (
                                "Você continua falando..."
                            )

                            # =================================
                            # ANSIEDADE SOBE
                            # =================================

                            estado_jogo.ansiedade += 8

                            # =================================
                            # PRESSÃO AUMENTA
                            # =================================

                            estado_jogo.velocidade_ansiedade += 0.7

                            self.temporizador_feedback = 1.2

                            self.indice += 1

                            if self.indice >= len(self.perguntas):

                                self.completado = True

                            break

        if self.temporizador_feedback > 0:

            self.temporizador_feedback -= 0.016

    # =====================================================
    # DRAW
    # =====================================================

    def desenhar(self, tela):

        if self.completado:
            return

        pergunta = self.pergunta_atual

        # =================================================
        # TÍTULO
        # =================================================

        titulo = self.fonte.render(
            "Apresentação",
            True,
            BRANCO
        )

        tela.blit(
            titulo,
            (70, 60)
        )

        # =================================================
        # PERGUNTA
        # =================================================

        render_pergunta = self.fonte.render(
            pergunta["pergunta"],
            True,
            BRANCO
        )

        tela.blit(
            render_pergunta,
            (70, 160)
        )

        mouse = pygame.mouse.get_pos()

        self.rects_botoes.clear()

        # =================================================
        # ESCOLHAS
        # =================================================

        for i, escolha in enumerate(
            pergunta["escolhas"]
        ):

            rect = self.criar_botao_responsivo(
                escolha,
                240 + i * 95
            )

            self.rects_botoes.append(rect)

            passando_mouse = rect.collidepoint(mouse)

            cor = PAINEL

            if passando_mouse:
                cor = (60, 60, 80)

            pygame.draw.rect(
                tela,
                cor,
                rect,
                border_radius=14
            )

            pygame.draw.rect(
                tela,
                BRANCO,
                rect,
                2,
                border_radius=14
            )

            render = self.fonte_pequena.render(
                escolha,
                True,
                BRANCO
            )

            tela.blit(
                render,
                (
                    rect.centerx
                    - render.get_width() // 2,

                    rect.centery
                    - render.get_height() // 2
                )
            )

        # =================================================
        # PROGRESSO
        # =================================================

        progresso = self.fonte_pequena.render(
            f"Pergunta {self.indice + 1}/9",
            True,
            CINZA
        )

        tela.blit(
            progresso,
            (70, 650)
        )

        # =================================================
        # FEEDBACK
        # =================================================

        if self.temporizador_feedback > 0:

            feedback = self.fonte_pequena.render(
                self.feedback,
                True,
                VERMELHO
            )

            tela.blit(
                feedback,
                (820, 650)
            )