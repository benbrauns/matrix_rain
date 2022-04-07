#
import pygame
import random
from src.constants import SPEED_MULT, ALLOWED_LETTERS, MIN_LETTER_TIME, MAX_LETTER_TIME
from src.rendered_text import RenderedText

class Letter:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.letter = None
        self.surface = None
        self.position = None
        self._reset_timer()
        self.new_letter()

    def _reset_timer(self):
        self.timer = random.randint(MIN_LETTER_TIME, MAX_LETTER_TIME)

    def new_letter(self):
        self.letter = random.choice(ALLOWED_LETTERS)
        self.surface = RenderedText.rendered[self.color][self.size][ALLOWED_LETTERS.index(self.letter)][self.letter]

    def update(self, dt):
        if self.timer <= 0:
            self._reset_timer()
        self.timer -= dt


