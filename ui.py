import pygame

from config import *


# -----------------------------------
# UI SYSTEM
# -----------------------------------

class UISystem:

    def __init__(self):

        # START VALUE
        self.display_anxiety = 10

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def update(self, real_anxiety, dt):

        # SMOOTH LERP
        smooth_speed = 5

        self.display_anxiety += (

            real_anxiety
            - self.display_anxiety

        ) * smooth_speed * dt

        # CLAMP
        self.display_anxiety = max(
            0,
            min(100, self.display_anxiety)
        )

    # -----------------------------------
    # DRAW
    # -----------------------------------

    def draw(self, screen, font):

        # -----------------------------------
        # CLEAN BACKGROUND
        # PREVENT TEXT BLEED
        # -----------------------------------

        pygame.draw.rect(
            screen,
            BACKGROUND,
            (15, 10, 420, 110)
        )

        # -----------------------------------
        # TEXT
        # -----------------------------------

        anxiety_text = font.render(
            f"Anxiety: {int(self.display_anxiety)}%",
            True,
            WHITE
        )

        screen.blit(
            anxiety_text,
            (40, 25)
        )

        # -----------------------------------
        # BAR RECT
        # -----------------------------------

        bg_rect = pygame.Rect(
            40,
            65,
            340,
            28
        )

        # -----------------------------------
        # SOLID PANEL
        # -----------------------------------

        panel = pygame.Surface(
            (340, 28),
            pygame.SRCALPHA
        )

        panel.fill((0, 0, 0, 0))

        pygame.draw.rect(
            panel,
            (22, 22, 32),
            (0, 0, 340, 28),
            border_radius=14
        )

        screen.blit(panel, (40, 65))

        # -----------------------------------
        # FILL WIDTH
        # -----------------------------------

        fill_width = int(
            (self.display_anxiety / 100)
            * 340
        )

        fill_rect = pygame.Rect(
            40,
            65,
            fill_width,
            28
        )

        # -----------------------------------
        # COLORS
        # -----------------------------------

        if self.display_anxiety < 35:

            color = (100, 200, 255)

        elif self.display_anxiety < 70:

            color = (255, 210, 90)

        else:

            color = (255, 90, 90)

        # -----------------------------------
        # MAIN BAR
        # -----------------------------------

        pygame.draw.rect(
            screen,
            color,
            fill_rect,
            border_radius=14
        )

        # -----------------------------------
        # BORDER
        # -----------------------------------

        pygame.draw.rect(
            screen,
            WHITE,
            bg_rect,
            2,
            border_radius=14
        )