import pygame

from config import *

from ui import UISystem
from breathing import BreathSystem
from thoughts import ThoughtSystem
from presentation import PresentationSystem


class GameState:

    def __init__(self, screen):

        self.screen = screen

        self.running = True

        self.font = pygame.font.Font(FONT, 28)

        self.big_font = pygame.font.Font(FONT, 62)

        self.ui = UISystem()

        self.state = "menu"

    # -----------------------------------
    # START GAME
    # -----------------------------------

    def start_game(self, questions):

        self.anxiety = 10

        self.ui.display_anxiety = self.anxiety

        self.game_timer = 0

        self.anxiety_rate = 2

        self.positive_chance = 0.18

        self.state = "playing"

        self.breath = BreathSystem()

        self.thoughts = ThoughtSystem()

        self.presentation = PresentationSystem(
            questions
        )

    # -----------------------------------
    # RESET
    # -----------------------------------

    def reset_to_menu(self):

        self.state = "menu"

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def update(self, dt, events):

        # -----------------------------------
        # MENU
        # -----------------------------------

        if self.state == "menu":

            mouse = pygame.mouse.get_pos()

            # UPDATED QUESTION COUNTS
            difficulties = [

                ("Easy", 10),

                ("Medium", 15),

                ("Hard", 20),

                ("Super Hard", 25)
            ]

            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i, (_, amount) in enumerate(difficulties):

                        rect = pygame.Rect(
                            WIDTH // 2 - 200,
                            240 + i * 100,
                            400,
                            70
                        )

                        if rect.collidepoint(mouse):

                            self.start_game(amount)

            return

        # -----------------------------------
        # END STATES
        # -----------------------------------

        if self.state in ["win", "fail"]:

            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.reset_to_menu()

            return

        # -----------------------------------
        # GAMEPLAY
        # -----------------------------------

        self.game_timer += dt

        # -----------------------------------
        # BREATHING
        # -----------------------------------

        breath_success = self.breath.update(
            events,
            dt
        )

        if breath_success:

            self.anxiety -= 15

            self.positive_chance += 0.04

            self.positive_chance = min(
                0.60,
                self.positive_chance
            )

        # -----------------------------------
        # PASSIVE ANXIETY
        # -----------------------------------

        if self.game_timer > 3:

            self.anxiety += dt * self.anxiety_rate

        # -----------------------------------
        # THOUGHTS
        # -----------------------------------

        thought_result = self.thoughts.update(
            events,
            self,
            dt
        )

        thought_anxiety, click_consumed = thought_result

        self.anxiety += thought_anxiety

        # -----------------------------------
        # QUESTIONS
        # -----------------------------------

        if not click_consumed:

            self.presentation.update(
                events,
                self
            )

        # -----------------------------------
        # CLAMP
        # -----------------------------------

        self.anxiety = max(
            0,
            min(MAX_ANXIETY, self.anxiety)
        )

        # -----------------------------------
        # UI UPDATE
        # -----------------------------------

        self.ui.update(
            self.anxiety,
            dt
        )

        # -----------------------------------
        # FAIL
        # -----------------------------------

        if self.anxiety >= 100:

            self.state = "fail"

        # -----------------------------------
        # WIN
        # -----------------------------------

        if self.presentation.completed:

            self.state = "win"

    # -----------------------------------
    # LOWER / CLEANER BLUR
    # -----------------------------------

    def apply_blur(self, surface):

        if self.anxiety < 35:

            return surface

        intensity = self.anxiety / 100

        scale = max(
            0.22,
            1 - (intensity * 0.9)
        )

        width = max(
            1,
            int(WIDTH * scale)
        )

        height = max(
            1,
            int(HEIGHT * scale)
        )

        # PASS 1
        small = pygame.transform.smoothscale(
            surface,
            (width, height)
        )

        blurred = pygame.transform.smoothscale(
            small,
            (WIDTH, HEIGHT)
        )

        # PASS 2
        if self.anxiety > 75:

            width2 = max(
                1,
                int(width * 0.7)
            )

            height2 = max(
                1,
                int(height * 0.7)
            )

            small2 = pygame.transform.smoothscale(
                blurred,
                (width2, height2)
            )

            blurred = pygame.transform.smoothscale(
                small2,
                (WIDTH, HEIGHT)
            )

        return blurred

    # -----------------------------------
    # MENU
    # -----------------------------------

    def draw_menu(self):

        title = self.big_font.render(
            "Hold Your Breath",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                100
            )
        )

        subtitle = self.font.render(
            "Choose a difficulty",
            True,
            GRAY
        )

        self.screen.blit(
            subtitle,
            (
                WIDTH // 2
                - subtitle.get_width() // 2,
                170
            )
        )

        # UPDATED TEXT
        difficulties = [

            ("Easy", "10 Questions"),

            ("Medium", "15 Questions"),

            ("Hard", "20 Questions"),

            ("Super Hard", "25 Questions")
        ]

        mouse = pygame.mouse.get_pos()

        for i, (name, desc) in enumerate(difficulties):

            rect = pygame.Rect(
                WIDTH // 2 - 200,
                240 + i * 100,
                400,
                70
            )

            hovering = rect.collidepoint(mouse)

            color = PANEL

            if hovering:

                color = (60, 60, 80)

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=16
            )

            pygame.draw.rect(
                self.screen,
                WHITE,
                rect,
                2,
                border_radius=16
            )

            text = self.font.render(
                f"{name} - {desc}",
                True,
                WHITE
            )

            self.screen.blit(
                text,
                (
                    rect.centerx
                    - text.get_width() // 2,

                    rect.centery
                    - text.get_height() // 2
                )
            )

    # -----------------------------------
    # END SCREEN
    # -----------------------------------

    def draw_end(self, win):

        if win:

            title = "You made it."

            lines = [

                "Nobody noticed the chaos inside your head.",

                "The presentation went well."
            ]

            color = WHITE

        else:

            title = "You lost control."

            lines = [

                "You could not control your breath",

                "and ran right to the bathroom",

                "to recollect yourself.",

                "You fainted."
            ]

            color = RED

        title_render = self.big_font.render(
            title,
            True,
            color
        )

        self.screen.blit(
            title_render,
            (
                WIDTH // 2
                - title_render.get_width() // 2,
                180
            )
        )

        for i, line in enumerate(lines):

            text = self.font.render(
                line,
                True,
                WHITE
            )

            self.screen.blit(
                text,
                (
                    WIDTH // 2
                    - text.get_width() // 2,

                    320 + i * 50
                )
            )

        restart = self.font.render(
            "Click to return to menu",
            True,
            GRAY
        )

        self.screen.blit(
            restart,
            (
                WIDTH // 2
                - restart.get_width() // 2,
                620
            )
        )

    # -----------------------------------
    # DRAW
    # -----------------------------------

    def draw(self):

        self.screen.fill(BACKGROUND)

        # MENU
        if self.state == "menu":

            self.draw_menu()

            return

        # WIN
        if self.state == "win":

            self.draw_end(True)

            return

        # FAIL
        if self.state == "fail":

            self.draw_end(False)

            return

        # -----------------------------------
        # GAMEPLAY SURFACE
        # -----------------------------------

        gameplay_surface = pygame.Surface(
            (WIDTH, HEIGHT)
        ).convert()

        gameplay_surface.fill(BACKGROUND)

        # -----------------------------------
        # DRAW GAMEPLAY
        # -----------------------------------

        self.presentation.draw(
            gameplay_surface
        )

        self.breath.draw(
            gameplay_surface
        )

        self.ui.draw(
            gameplay_surface,
            self.font
        )

        # -----------------------------------
        # BLUR
        # -----------------------------------

        blurred_surface = self.apply_blur(
            gameplay_surface
        )

        self.screen.blit(
            blurred_surface,
            (0, 0)
        )

        # -----------------------------------
        # SHARP THOUGHTS
        # -----------------------------------

        self.thoughts.draw(
            self.screen
        )