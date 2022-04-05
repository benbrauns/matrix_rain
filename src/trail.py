#
import random
import pygame.display
from src.utils import weighted_random_size, make
from src.letter import Letter

class Trail:
    def __init__(self, color):
        self.length = random.randint(10, 30)
        self.color = color
        self.letters = None
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())
        self.new_letters()

    def new_letters(self):
        self.letters = make(Letter, self.length, args=(*weighted_random_size(),
                                                       (random.randint(0, self.bounds.width), random.randint(-200, 0)),
                                                       self.color))

    def update_bounds(self, new_bounds):
        self.bounds = new_bounds
        [letter.update_bounds(new_bounds) for letter in self.letters]

    def update(self, dt):
        for letter in self.letters:
            letter.update(dt)

    def draw(self, surface):
        for letter in self.letters:
            letter.draw(surface)