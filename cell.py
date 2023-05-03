import random
import pygame as pg

from constants import (
    UP,
    DOWN,
    LEFT,
    RIGHT,
    SIZE,
    DIM,
    SHOW_ENTROPY,
    error_image,
)


class Cell:
    def __init__(self, position: tuple, size=SIZE, tiles: list = []):
        self.position: tuple = position
        self.size: int = size
        self.possibilities = tiles.copy()

    @property
    def collapsed(self):
        return len(self.possibilities) == 1

    @property
    def tile(self):
        return self.possibilities[0]

    @property
    def entropy(self):
        return len(self.possibilities)

    def collapse(self):
        self.possibilities = [random.choice(self.possibilities)]

    def update_possible_tiles(self, rule: int, from_dir: int, cells: list):
        if not self.collapsed:
            self.possibilities = [tile for tile in self.possibilities if tile.rules[from_dir] == rule]
            if self.entropy == 1:
                self.collapse()
                self.update_neighbours(cells)

    def update_neighbours(self, cells):
        if self.position[0] < DIM - 1:
            neighbour_right = cells[self.position[0] + 1][self.position[1]]
            neighbour_right.update_possible_tiles(self.tile.rules[RIGHT], from_dir=LEFT, cells=cells)

        if self.position[0] > 0:
            neighbour_right = cells[self.position[0] - 1][self.position[1]]
            neighbour_right.update_possible_tiles(self.tile.rules[LEFT], from_dir=RIGHT, cells=cells)

        if self.position[1] < DIM - 1:
            neighbour_right = cells[self.position[0]][self.position[1] + 1]
            neighbour_right.update_possible_tiles(self.tile.rules[DOWN], from_dir=UP, cells=cells)

        if self.position[0] > 0:
            neighbour_right = cells[self.position[0]][self.position[1] - 1]
            neighbour_right.update_possible_tiles(self.tile.rules[UP], from_dir=DOWN, cells=cells)

    def display(self, window: pg.Surface):
        if self.entropy == 0:
            window.blit(error_image, (self.position[0] * self.size, self.position[1] * self.size))

        if self.collapsed:
            window.blit(self.tile.base_image, (self.position[0] * self.size, self.position[1] * self.size))
        elif SHOW_ENTROPY:
            if self.entropy != 0:
                text = pg.font.SysFont("Arial", 10).render(str(self.entropy), True, (255, 255, 255))
            else:
                text = pg.font.SysFont("Arial", 10).render(str(self.entropy), True, (255, 0, 0))
            window.blit(text, (self.position[0] * self.size, self.position[1] * self.size))
            # for index, tile in enumerate(self.possibilities):
            #     window.blit(pg.transform.scale(tile.base_image, (10, 10)), (self.position[0] * self.size, self.position[1] * self.size  + (index * 10)))
            #     text = pg.font.SysFont("Arial", 10).render(str(tile.rules), True, (255, 255, 255))
            #     window.blit(text, (self.position[0] * self.size + 10, self.position[1] * self.size + (index * 10)))

    def __repr__(self):
        return f"Cell({self.position}, {len(self.possibilities)})"
