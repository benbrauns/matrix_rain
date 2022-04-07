#
import pygame
import random
from src.constants import GREEN, ALLOWED_LETTERS, MIN_LETTER_TIME, MAX_LETTER_TIME
from src.rendered_text import RenderedText

class Letter(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.color = GREEN
        self.surface = None
        self.position = None
        self.changed = False
        self._reset_timer()
        self.new_letter()

    def _reset_timer(self):
        self.timer = random.randint(MIN_LETTER_TIME, MAX_LETTER_TIME)

    def new_letter(self):
        letter = random.choice(ALLOWED_LETTERS)
        self.surface = RenderedText.rendered[self.color][self.size][ALLOWED_LETTERS.index(letter)][letter]
        self.changed = True

    def update(self, dt):
        if self.timer <= 0:
            self.new_letter()
            self._reset_timer()
        self.timer -= dt

    def draw(self, surface):
        self.changed = False
        center_x = surface.get_width() // 2 - self.surface.get_width() // 2
        surface.blit(self.surface, (center_x, self.surface.get_height() * self.position))
