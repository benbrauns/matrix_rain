#
import pygame
import random
from src.constants import PADDING, SPEED_MULT, ALLOWED_LETTERS, MIN_LETTER_TIME, MAX_LETTER_TIME
from src.rendered_text import RenderedText

class Letter(pygame.sprite.Sprite):
    def __init__(self, group, size, color, velocity, trail):
        super().__init__(group)
        self.trail = trail
        self.size = size
        self.color = color
        self.letter = None
        self.image = None
        self.position = None
        self.location = None
        self.rect = None
        self.velocity = velocity
        self._reset_timer()
        self.new_letter()


    #This has a bug in it cause they are all aligned left but I'm not worried about it right now but it just assigns the postion to each letter so they can be updated with velocity
    def getRect(self,midtop): 
        # margin = self.image.get_height() * 0.10
        self.location = (midtop + pygame.math.Vector2(0,(self.image.get_height() + PADDING) * self.position + self.image.get_height() / 2))
        self.rect = self.image.get_rect(center=self.location)

    def _reset_timer(self):
        self.timer = random.randint(MIN_LETTER_TIME, MAX_LETTER_TIME)

    def new_letter(self):
        self.letter = random.choice(ALLOWED_LETTERS)
        self.image = RenderedText.rendered[self.color][self.size][ALLOWED_LETTERS.index(self.letter)][self.letter]

    def update(self, dt):
        self.rect.center += self.velocity
        if self.timer <= 0:
            self.new_letter()
            self._reset_timer()
            self.trail.letter_changed = True
        self.timer -= dt
        if self.rect.top > pygame.display.get_window_size()[1]:
            self.kill()
            del self
        


