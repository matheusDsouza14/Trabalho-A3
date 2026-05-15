import pygame
import random

from config import *


# =========================================================
# QUESTION DATABASE
# =========================================================
# ADD AS MANY QUESTIONS AS YOU WANT
#
# FORMAT:
#
# {
#     "question": "Question text",
#
#     "choices": [
#         "Choice 1",
#         "Choice 2",
#         "Choice 3",
#         "Choice 4"
#     ],
#
#     "correct": index_of_correct_answer
# }
#
# IMPORTANT:
# - ALWAYS USE 4 CHOICES
# - correct MUST MATCH THE INDEX
# =========================================================

QUESTION_POOL = [

    {
        "question": "What is the main topic of your essay?",

        "choices": [
            "Social anxiety in education",
            "Marine biology",
            "Ancient warfare",
            "Quantum mechanics"
        ],

        "correct": 0
    },

    {
        "question": "What symptom is discussed first?",

        "choices": [
            "Aggression",
            "Panic response",
            "Memory loss",
            "Insomnia"
        ],

        "correct": 1
    },

    {
        "question": "What helps reduce anxiety symptoms?",

        "choices": [
            "Avoidance",
            "Controlled breathing",
            "Isolation",
            "Shouting"
        ],

        "correct": 1
    },

    {
        "question": "What causes distorted perception?",

        "choices": [
            "Panic overload",
            "Lack of sleep",
            "Bright lights",
            "Background noise"
        ],

        "correct": 0
    },

    {
        "question": "What is the player truly fighting?",

        "choices": [
            "The teacher",
            "The classroom",
            "Their own thoughts",
            "Homework"
        ],

        "correct": 2
    },

    {
        "question": "What helps regain control?",

        "choices": [
            "Breathing slowly",
            "Leaving the room",
            "Ignoring emotions",
            "Shouting"
        ],

        "correct": 0
    },

    {
        "question": "What physical symptom appears first?",

        "choices": [
            "Voice shaking",
            "Coughing",
            "Blindness",
            "Headache"
        ],

        "correct": 0
    },

    {
        "question": "What is the game's main message?",

        "choices": [
            "Fear controls reality",
            "Anxiety distorts perception",
            "Presentations are pointless",
            "People are always judging"
        ],

        "correct": 1
    }
]


# =========================================================
# PRESENTATION SYSTEM
# =========================================================

class PresentationSystem:

    def __init__(self, amount):

        # -------------------------------------------------
        # SAFE QUESTION COUNT
        # -------------------------------------------------

        question_count = min(
            amount,
            len(QUESTION_POOL)
        )

        # -------------------------------------------------
        # RANDOM QUESTIONS
        # NO DUPLICATES
        # -------------------------------------------------

        self.questions = random.sample(
            QUESTION_POOL,
            question_count
        )

        self.index = 0

        self.completed = False

        self.font = pygame.font.Font(FONT, 34)

        self.small_font = pygame.font.Font(FONT, 24)

        self.feedback = ""

        self.feedback_timer = 0

    # -----------------------------------------------------
    # CURRENT QUESTION
    # -----------------------------------------------------

    @property
    def current_question(self):

        return self.questions[self.index]

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def update(self, events, game_state):

        if self.completed:
            return

        mouse = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    for i in range(4):

                        rect = pygame.Rect(
                            120,
                            250 + i * 90,
                            700,
                            60
                        )

                        if rect.collidepoint(mouse):

                            # -----------------------------
                            # CORRECT
                            # -----------------------------

                            if i == self.current_question["correct"]:

                                self.feedback = "You kept going."

                                game_state.anxiety -= 8

                            # -----------------------------
                            # WRONG
                            # -----------------------------

                            else:

                                self.feedback = "Your thoughts spiral."

                                game_state.anxiety += 18

                            # -----------------------------
                            # PRESSURE BUILDS
                            # -----------------------------

                            game_state.anxiety_rate += 0.7

                            self.feedback_timer = 1.5

                            self.index += 1

                            # -----------------------------
                            # FINISH
                            # -----------------------------

                            if self.index >= len(self.questions):

                                self.completed = True

                            break

        # FEEDBACK TIMER
        if self.feedback_timer > 0:

            self.feedback_timer -= 0.016

    # -----------------------------------------------------
    # DRAW
    # -----------------------------------------------------

    def draw(self, screen):

        if self.completed:
            return

        q = self.current_question

        # TITLE
        title = self.font.render(
            "Class Presentation",
            True,
            WHITE
        )

        screen.blit(title, (70, 60))

        # QUESTION
        question = self.font.render(
            q["question"],
            True,
            WHITE
        )

        screen.blit(question, (70, 150))

        mouse = pygame.mouse.get_pos()

        # CHOICES
        for i, choice in enumerate(q["choices"]):

            rect = pygame.Rect(
                120,
                250 + i * 90,
                700,
                60
            )

            hovering = rect.collidepoint(mouse)

            color = PANEL

            if hovering:

                color = (60, 60, 80)

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=14
            )

            pygame.draw.rect(
                screen,
                WHITE,
                rect,
                2,
                border_radius=14
            )

            text = self.small_font.render(
                choice,
                True,
                WHITE
            )

            screen.blit(
                text,
                (
                    rect.x + 20,
                    rect.y + 18
                )
            )

        # PROGRESS
        progress = self.small_font.render(
            f"Question {self.index + 1}/{len(self.questions)}",
            True,
            GRAY
        )

        screen.blit(progress, (70, 650))

        # FEEDBACK
        if self.feedback_timer > 0:

            feedback = self.small_font.render(
                self.feedback,
                True,
                GREEN
            )

            screen.blit(feedback, (900, 650))