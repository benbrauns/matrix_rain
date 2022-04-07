#
import random
import pygame.display
from src.utils import weighted_random_size, make
from src.letter import Letter
from src.constants import SPEED_MULT

class Trail:
    def __init__(self, color):
        self.length = random.randint(10, 30)
        self.color = color
        self.letters = None
        self.surface = None
        self.rect = None
        self.velocity = pygame.Vector2((0, 0))
        self.new_letters()

    def new_letters(self):
        window_width = pygame.display.get_window_size()[0]
        self.letters = make(Letter, self.length, args=(*weighted_random_size(), self.color))


        width = self.letters[0].surface.get_width() * 2
        height = self.letters[0].surface.get_height() * len(self.letters)
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey('black')
        x = random.randint(0, window_width)
        y = random.randint(-200 + -height, -height)
        self.rect = self.surface.get_rect(center=(x, y))
        for letter in self.letters:
            center_x = self.surface.get_width() // 2 - letter.surface.get_width() // 2
            self.surface.blit(letter.surface, (center_x, letter.surface.get_height() * letter.position))
        self.velocity.update(0, self.letters[0].size * SPEED_MULT)
        # Create surface and blit new letters

    def update(self, dt):
        # Blit onto Trail surface if new changes
        [letter.update(dt) for letter in self.letters]
        self.rect.center += self.velocity

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

