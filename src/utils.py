#
import random
from src.letter import Letter
from src.rendered_text import RenderedText
from src.constants import GREENISH_WHITE

def make(class_name, total=1, args=None):
    objects = []
    last = total - 1
    for i in range(total):
        new_object = class_name(*args)
        if isinstance(new_object, Letter):
            if i == last:
                new_object.color = GREENISH_WHITE
                new_object.new_letter()
            new_object.position = i
        objects.append(new_object)
    return objects

def weighted_random_size():
    font_objects_list = list(RenderedText.font_objects.keys())
    divisor = len(font_objects_list) // 3
    small = random.choice(font_objects_list[:divisor])
    medium = random.choice(font_objects_list[divisor:divisor*2])
    large = random.choice(font_objects_list[divisor*2:])

    choice = random.choices([small,medium,large], weights=(0.70, 0.25, 0.05))
    return choice

