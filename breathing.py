import pygame
import math

from config import *


class BreathSystem:

    def __init__(self):

        self.base_radius = 55

        self.radius = self.base_radius

        self.max_radius = 75

        self.holding = False

        self.hold_time = 0

        self.completed = False

        self.center = (
            WIDTH - 120,
            HEIGHT - 120
        )

        self.font = pygame.font.Font(
            FONT,
            22
        )

        # ANIMATION TIMER
        self.anim_timer = 0

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def update(self, events, dt):

        mouse = pygame.mouse.get_pos()

        self.completed = False

        self.anim_timer += dt

        # BUTTON COLLISION
        distance = math.dist(
            mouse,
            self.center
        )

        hovering = distance <= self.radius

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # -----------------------------------
        # HOLDING BUTTON
        # -----------------------------------

        if hovering and mouse_pressed:

            self.holding = True

            self.hold_time += dt

            # -----------------------------------
            # BREATHING PULSE
            # -----------------------------------

            pulse = math.sin(
                self.anim_timer * 4
            ) * 8

            self.radius = self.base_radius + pulse

            # SUCCESS
            if self.hold_time >= 2:

                self.completed = True

                self.hold_time = 0

        else:

            self.holding = False

            self.hold_time = 0

            # SMOOTH RETURN
            self.radius += (
                self.base_radius - self.radius
            ) * 0.15

        return self.completed

    # -----------------------------------
    # DRAW
    # -----------------------------------

    def draw(self, screen):

        # OUTER GLOW
        glow_surface = pygame.Surface(
            (220, 220),
            pygame.SRCALPHA
        )

        glow_radius = int(self.radius + 18)

        pygame.draw.circle(
            glow_surface,
            (120, 180, 255, 40),
            (110, 110),
            glow_radius
        )

        screen.blit(
            glow_surface,
            (
                self.center[0] - 110,
                self.center[1] - 110
            )
        )

        # MAIN BUTTON
        color = (120, 170, 255)

        if self.holding:

            color = (170, 210, 255)

        pygame.draw.circle(
            screen,
            color,
            self.center,
            int(self.radius)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            self.center,
            int(self.radius),
            4
        )

        # TEXT
        if self.holding:

            label = "Breathe..."

        else:

            label = "Hold"

        text = self.font.render(
            label,
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                self.center[0]
                - text.get_width() // 2,

                self.center[1]
                - text.get_height() // 2
            )
        )

        # HOLD PROGRESS
        progress = min(
            self.hold_time / 2,
            1
        )

        progress_width = 120

        bar_rect = pygame.Rect(
            self.center[0] - 60,
            self.center[1] + 85,
            progress_width,
            10
        )

        pygame.draw.rect(
            screen,
            (40, 40, 50),
            bar_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (120, 200, 255),
            (
                bar_rect.x,
                bar_rect.y,
                progress_width * progress,
                10
            ),
            border_radius=8
        )