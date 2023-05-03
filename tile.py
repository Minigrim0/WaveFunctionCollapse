from hashlib import sha256
import pygame as pg
from collections import deque


from constants import UP, DOWN, LEFT, RIGHT, SIZE, DIM


class Tile:
    def __init__(self, base_image: pg.Surface, rotation: int, rules: list = [], infer_from_image: bool = False):
        self.rotation = 0  # 0, 1, 2, 3
        self.base_image = pg.transform.scale(base_image, (SIZE, SIZE))
        self.rules = deque(rules)
        self.rotate(rotation)
        if infer_from_image:
            self.rules = deque([0, 0, 0, 0])
            self.infer_rules()

    def infer_rules(self):
        # Get first row of pixels
        first_row = ""
        for x in range(self.base_image.get_width()):
            first_row += f"{str(self.base_image.get_at((x, 0)))}, "
        first_row = first_row[:-2]
        self.rules[UP] = sha256(first_row.encode()).hexdigest()

        # Get last row of pixels
        last_row = ""
        for x in range(self.base_image.get_width()):
            last_row += f"{str(self.base_image.get_at((x, self.base_image.get_height() - 1)))}, "
        last_row = last_row[:-2]
        self.rules[DOWN] = sha256(last_row.encode()).hexdigest()

        # Get first column of pixels
        first_column = ""
        for y in range(self.base_image.get_height()):
            first_column += f"{str(self.base_image.get_at((0, y)))}, "
        first_column = first_column[:-2]
        self.rules[LEFT] = sha256(first_column.encode()).hexdigest()

        # Get last column of pixels
        last_column = ""
        for y in range(self.base_image.get_height()):
            last_column += f"{str(self.base_image.get_at((self.base_image.get_width() - 1, y)))}, "
        last_column = last_column[:-2]
        self.rules[RIGHT] = sha256(last_column.encode()).hexdigest()

    def rotate(self, rotation: int):
        self.rotation = rotation
        self.base_image = pg.transform.rotate(self.base_image, rotation * 90)
        if rotation > 0:
            self.rules.rotate(-rotation)  # Rules are inverted when rotating
