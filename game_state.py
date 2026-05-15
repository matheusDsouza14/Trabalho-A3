import pygame

from config import *
from ui import SistemaUI
from breathing import SistemaRespiracao
from thoughts import SistemaPensamentos
from presentation import SistemaApresentacao


class EstadoJogo:

    def __init__(self, tela):

        self.tela = tela

        self.rodando = True

        self.fonte = pygame.font.Font(
            FONTE,
            int(30 * 1.07)
        )

        self.fonte_grande = pygame.font.Font(
            FONTE,
            int(66 * 1.07)
        )

        self.ui = SistemaUI()

        self.estado = "jogando"

        self.iniciar_jogo()

    # =====================================================
    # INICIAR JOGO
    # =====================================================

    def iniciar_jogo(self):

        self.ansiedade = 10

        self.ui.ansiedade_visual = self.ansiedade

        self.temporizador_jogo = 0

        self.velocidade_ansiedade = 2

        self.chance_positiva = 0.18

        self.estado = "jogando"

        self.respiracao = SistemaRespiracao()

        self.pensamentos = SistemaPensamentos()

        # =================================================
        # 9 PERGUNTAS
        # =================================================

        self.apresentacao = SistemaApresentacao(9)

    # =====================================================
    # REINICIAR
    # =====================================================

    def reiniciar(self):

        self.iniciar_jogo()

    # =====================================================
    # UPDATE
    # =====================================================

    def atualizar(self, dt, eventos):

        if self.estado in ["vitoria", "derrota"]:

            for evento in eventos:

                if evento.type == pygame.MOUSEBUTTONDOWN:

                    self.reiniciar()

            return

        self.temporizador_jogo += dt

        # =================================================
        # RESPIRAÇÃO
        # =================================================

        sucesso_respiracao = self.respiracao.atualizar(
            eventos,
            dt
        )

        if sucesso_respiracao:

            self.ansiedade -= 15

            self.chance_positiva += 0.04

            self.chance_positiva = min(
                0.60,
                self.chance_positiva
            )

        # =================================================
        # ANSIEDADE PASSIVA
        # =================================================

        if self.temporizador_jogo > 3:

            self.ansiedade += (
                dt * self.velocidade_ansiedade
            )

        # =================================================
        # PENSAMENTOS
        # =================================================

        resultado_pensamentos = self.pensamentos.atualizar(
            eventos,
            self,
            dt
        )

        mudanca_ansiedade, clique_consumido = (
            resultado_pensamentos
        )

        self.ansiedade += mudanca_ansiedade

        # =================================================
        # PERGUNTAS
        # =================================================

        if not clique_consumido:

            self.apresentacao.atualizar(
                eventos,
                self
            )

        # =================================================
        # LIMITADOR
        # =================================================

        self.ansiedade = max(
            0,
            min(
                ANSIEDADE_MAXIMA,
                self.ansiedade
            )
        )

        # =================================================
        # UI
        # =================================================

        self.ui.atualizar(
            self.ansiedade,
            dt
        )

        # =================================================
        # DERROTA
        # =================================================

        if self.ansiedade >= 100:

            self.estado = "derrota"

        # =================================================
        # VITÓRIA
        # =================================================

        if self.apresentacao.completado:

            self.estado = "vitoria"

    # =====================================================
    # BLUR
    # =====================================================

    def aplicar_blur(self, superficie):

        if self.ansiedade < 35:

            return superficie

        intensidade = self.ansiedade / 100

        escala = max(
            0.22,
            1 - (intensidade * 0.9)
        )

        largura = max(
            1,
            int(LARGURA * escala)
        )

        altura = max(
            1,
            int(ALTURA * escala)
        )

        pequena = pygame.transform.smoothscale(
            superficie,
            (largura, altura)
        )

        borrada = pygame.transform.smoothscale(
            pequena,
            (LARGURA, ALTURA)
        )

        return borrada

    # =====================================================
    # TELA FINAL
    # =====================================================

    def desenhar_final(self, venceu):

        if venceu:

            titulo = "Você conseguiu."

            linhas = [
                "Ninguém percebeu o caos na sua mente.",
                "Tudo deu certo :)",
                "Parabens!!!"
            ]

            cor = BRANCO

        else:

            titulo = "Você perdeu o controle."

            linhas = [
                "Você não conseguiu",
                "controlar sua respiração.",
                "A ansiedade venceu."
            ]

            cor = VERMELHO

        render_titulo = self.fonte_grande.render(
            titulo,
            True,
            cor
        )

        self.tela.blit(
            render_titulo,
            (
                LARGURA // 2
                - render_titulo.get_width() // 2,
                180
            )
        )

        for i, linha in enumerate(linhas):

            render = self.fonte.render(
                linha,
                True,
                BRANCO
            )

            self.tela.blit(
                render,
                (
                    LARGURA // 2
                    - render.get_width() // 2,
                    320 + i * 50
                )
            )

    # =====================================================
    # DRAW
    # =====================================================

    def desenhar(self):

        self.tela.fill(FUNDO)

        if self.estado == "vitoria":

            self.desenhar_final(True)

            return

        if self.estado == "derrota":

            self.desenhar_final(False)

            return

        superficie_jogo = pygame.Surface(
            (LARGURA, ALTURA)
        ).convert()

        superficie_jogo.fill(FUNDO)

        self.apresentacao.desenhar(
            superficie_jogo
        )

        self.respiracao.desenhar(
            superficie_jogo
        )

        self.ui.desenhar(
            superficie_jogo,
            self.fonte
        )

        superficie_borrada = self.aplicar_blur(
            superficie_jogo
        )

        self.tela.blit(
            superficie_borrada,
            (0, 0)
        )

        self.pensamentos.desenhar(
            self.tela
        )