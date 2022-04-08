#
from copy import copy
import random
import pygame.display
from src.utils import weighted_random_size, make
from src.letter import Letter
from src.constants import SPEED_MULT

class Trail(pygame.sprite.Sprite):
    def __init__(self, color, group, letter_group):
        super().__init__(group)
        self.length = random.randint(10, 30)
        self.color = color
        self.letter_size = weighted_random_size()[0]
        self.velocity = pygame.Vector2((0, 0))
        self.velocity.update(0, self.letter_size * SPEED_MULT)
        self.letters = self.createLetters(letter_group)
        self.group = group
        self.letter_group = letter_group
        self.image = None
        self.rect = None
        self.new_letters()


    def createLetters(self, letter_group):
        letters = []
        for i in range(self.length):
            letter = Letter(letter_group, self.letter_size, self.color, self.velocity)
            letter.position = i

            letter_group.add(letter)
            letters.append(letter)
        return letters

    def new_letters(self):
        window_width = pygame.display.get_window_size()[0]
        width = self.letters[0].image.get_width() * 2
        height = self.letters[0].image.get_height() * len(self.letters)
        # self.image = pygame.Surface((width, height))
        # self.image.set_colorkey('black')
        x = random.randint(-100, window_width)
        y = random.randint(-200 + -height, -height)
        self.rect = pygame.Rect((x,y),(width,height))
        for letter in self.letters:
            letter.getRect(self.rect.midtop)
        
    def delete(self):
        for letter in self.letters:
            letter.kill()
            del letter
        self.kill()
        del self

    def update(self):
        #checks if the trail should be removed
        self.rect.center += self.velocity
        if self.rect.top > pygame.display.get_window_size()[1]:
            self.delete()



