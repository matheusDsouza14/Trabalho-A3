import pygame
import random

from config import *


# =========================================================
# NEGATIVE THOUGHT DATABASE
# =========================================================
# ADD AS MANY AS YOU WANT
# =========================================================

NEGATIVE_THOUGHTS = [

    "Everyone noticed your voice shaking",

    "You're embarrassing yourself",

    "You forgot everything",

    "They're judging you",

    "You're failing",

    "You sound nervous",

    "They think you're stupid",

    "Everyone is staring at you",

    "You're ruining the presentation",

    "You should leave the room"
]


# =========================================================
# POSITIVE THOUGHT DATABASE
# =========================================================
# ADD AS MANY AS YOU WANT
# =========================================================

POSITIVE_THOUGHTS = [

    "Just keep going",

    "Breathe slowly",

    "Nobody expects perfection",

    "You're okay",

    "You can do this",

    "Focus on the presentation",

    "You're still standing",

    "Keep breathing",

    "You're doing better than you think",

    "One step at a time"
]


# =========================================================
# THOUGHT
# =========================================================

class Thought:

    def __init__(self, text, positive):

        self.text = text

        self.positive = positive

        self.timer = 5

        self.clicked = False

        self.font = pygame.font.Font(FONT, 28)

        self.width = 500

        self.height = 120

        # RANDOM POSITION
        while True:

            self.x = random.randint(120, 650)

            self.y = random.randint(80, 500)

            # AVOID BREATH BUTTON
            if not (
                self.x > 850 and
                self.y > 450
            ):
                break

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def update(self, dt):

        self.timer -= dt

    # -----------------------------------------------------
    # DRAW
    # -----------------------------------------------------

    def draw(self, screen):

        if self.positive:

            bg = (40, 90, 60)

            border = GREEN

        else:

            bg = (90, 40, 40)

            border = RED

        pygame.draw.rect(
            screen,
            bg,
            self.rect,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            border,
            self.rect,
            4,
            border_radius=18
        )

        text = self.font.render(
            self.text,
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                self.rect.centerx
                - text.get_width() // 2,

                self.rect.centery
                - text.get_height() // 2
            )
        )


# =========================================================
# THOUGHT SYSTEM
# =========================================================

class ThoughtSystem:

    def __init__(self):

        self.thoughts = []

        self.spawn_timer = 0

    # -----------------------------------------------------
    # RANDOM THOUGHT
    # -----------------------------------------------------

    def create_random_thought(self, positive):

        if positive:

            text = random.choice(
                POSITIVE_THOUGHTS
            )

        else:

            text = random.choice(
                NEGATIVE_THOUGHTS
            )

        return Thought(text, positive)

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def update(self, events, game_state, dt):

        self.spawn_timer += dt

        anxiety_change = 0

        click_consumed = False

        # -------------------------------------------------
        # SPAWN SPEED
        # -------------------------------------------------

        spawn_speed = 2.5

        if game_state.anxiety > 50:
            spawn_speed = 1.8

        if game_state.anxiety > 75:
            spawn_speed = 1.2

        # -------------------------------------------------
        # SPAWN RANDOM THOUGHT
        # -------------------------------------------------

        if self.spawn_timer >= spawn_speed:

            self.spawn_timer = 0

            positive = (

                random.random()

                < game_state.positive_chance
            )

            self.thoughts.append(
                self.create_random_thought(
                    positive
                )
            )

        # -------------------------------------------------
        # CLICK DETECTION
        # -------------------------------------------------

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    for thought in reversed(self.thoughts):

                        if thought.rect.collidepoint(event.pos):

                            click_consumed = True

                            thought.clicked = True

                            # ONLY POSITIVE
                            # REDUCES ANXIETY
                            if thought.positive:

                                anxiety_change -= 20

                            break

        # -------------------------------------------------
        # UPDATE THOUGHTS
        # -------------------------------------------------

        for thought in self.thoughts:

            thought.update(dt)

            if thought.timer <= 0:

                if not thought.clicked:

                    if not thought.positive:

                        anxiety_change += 18

        # -------------------------------------------------
        # REMOVE
        # -------------------------------------------------

        self.thoughts = [

            t for t in self.thoughts

            if t.timer > 0 and not t.clicked
        ]

        return anxiety_change, click_consumed

    # -----------------------------------------------------
    # DRAW
    # -----------------------------------------------------

    def draw(self, screen):

        for thought in self.thoughts:

            thought.draw(screen)