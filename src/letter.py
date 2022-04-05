#
import pygame
import random
from src.constants import SPEED_MULT, ALLOWED_LETTERS, MIN_LETTER_TIME, MAX_LETTER_TIME
from src.rendered_text import RenderedText

class Letter:
    def __init__(self, size, position, color):
        self.size = size
        self.color = color
        self.letter = None
        self.surface = None
        self.rect = None
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())
        self.velocty = pygame.Vector2(0, self.size * SPEED_MULT)
        self._reset_timer()
        self.new_letter(position)

    def _reset_timer(self):
        self.timer = random.randint(MIN_LETTER_TIME, MAX_LETTER_TIME)

    def new_letter(self, position):
        self.letter = random.choice(ALLOWED_LETTERS)
        self.surface = RenderedText.rendered_letters[self.color][self.size][ALLOWED_LETTERS.index(self.letter)][self.letter]
        self.rect = self.surface.get_rect(center=position)
        self.velocty.update(0, self.size * SPEED_MULT)

    def on_screen(self):
        return -self.rect.height < self.rect.y < self.bounds.height

    def update_bounds(self, new_bounds):
        self.bounds = new_bounds

    def update(self, dt):
        self.rect.center += self.velocty
        if self.timer <= 0:
            if self.on_screen():
                self.new_letter(self.rect.center)
            self._reset_timer()
        self.timer -= dt

    def draw(self, surface):
        if self.on_screen():
            surface.blit(self.surface, self.rect)

