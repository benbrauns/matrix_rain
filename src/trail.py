#
import random
import pygame.display
from src.utils import weighted_random_size, make
from src.letter import Letter
from src.constants import SPEED_MULT

class Trail(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.length = random.randint(10, 30)
        self.letters = None
        self.surface = None
        self.rect = None
        self.velocity = pygame.Vector2((0, 0))
        self.new_letters()

    def new_letters(self):
        self.letters = make(Letter, self.length, args=(*weighted_random_size(),))
        self.velocity.update(0, self.letters[0].size * SPEED_MULT)
        self.update_surface()


    def update_surface(self):
        window_width = pygame.display.get_window_size()[0]
        width = self.letters[0].surface.get_width() * 2
        #print(width)
        height = self.letters[0].surface.get_height() * len(self.letters)

        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey('black')
        if not self.rect:
            x = random.randint(0, window_width)
            y = random.randint(-height - 200, -height)
            self.rect = self.surface.get_rect(center=(x, y))
        for letter in self.letters:
            letter.draw(self.surface)

    def update(self, dt):
        # Blit onto Trail surface if new changes
        [letter.update(dt) for letter in self.letters]
        self.rect.center += self.velocity

    def draw(self, surface):
        #[letter.draw(self.surface) for letter in self.letters]
        if any(letter.changed for letter in self.letters):
            self.update_surface()
        surface.blit(self.surface, self.rect)

