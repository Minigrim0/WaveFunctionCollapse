import time
import random
import pygame as pg
from collections import deque

pg.init()
window = pg.display.set_mode((500, 500))

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIM = 50
SIZE = 10
SHOW_ENTROPY = False
SPEED = 10


class Tile:
    def __init__(self, base_image: pg.Surface, rotation: int, rules: list):
        self.rotation = 0  # 0, 1, 2, 3
        self.base_image = pg.transform.scale(base_image, (SIZE, SIZE))
        self.rules = deque(rules)
        self.rotate(rotation)

    def rotate(self, rotation: int):
        self.rotation = rotation
        self.base_image = pg.transform.rotate(self.base_image, rotation * 90)
        if rotation > 0:
            self.rules.rotate(-rotation)  # Rules are inverted when rotating


tiles = [
    Tile(pg.image.load("tiles/t.png"), 0, [0, 1, 1, 1]),
    Tile(pg.image.load("tiles/t.png"), 1, [0, 1, 1, 1]),
    Tile(pg.image.load("tiles/t.png"), 2, [0, 1, 1, 1]),
    Tile(pg.image.load("tiles/t.png"), 3, [0, 1, 1, 1]),
    Tile(pg.image.load("tiles/l.png"), 0, [1, 0, 0, 1]),
    Tile(pg.image.load("tiles/l.png"), 1, [1, 0, 0, 1]),
    Tile(pg.image.load("tiles/l.png"), 2, [1, 0, 0, 1]),
    Tile(pg.image.load("tiles/l.png"), 3, [1, 0, 0, 1]),
    Tile(pg.image.load("tiles/i.png"), 0, [1, 0, 1, 0]),
    Tile(pg.image.load("tiles/i.png"), 1, [1, 0, 1, 0]),
    Tile(pg.image.load("tiles/i.png"), 2, [1, 0, 1, 0]),
    Tile(pg.image.load("tiles/i.png"), 3, [1, 0, 1, 0]),
]


class Cell:
    def __init__(self, position: tuple, size=SIZE):
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

    def update_possible_tiles(self, rule: int, from_dir: int):
        if not self.collapsed:
            self.possibilities = [tile for tile in self.possibilities if tile.rules[from_dir] == rule]
            if self.entropy == 1:
                self.collapse()
                self.update_neighbours(cells)

    def update_neighbours(self, cells):
        if self.position[0] < DIM - 1:
            neighbour_right = cells[self.position[0] + 1][self.position[1]]
            neighbour_right.update_possible_tiles(self.tile.rules[RIGHT], from_dir=LEFT)

        if self.position[0] > 0:
            neighbour_right = cells[self.position[0] - 1][self.position[1]]
            neighbour_right.update_possible_tiles(self.tile.rules[LEFT], from_dir=RIGHT)

        if self.position[1] < DIM - 1:
            neighbour_right = cells[self.position[0]][self.position[1] + 1]
            neighbour_right.update_possible_tiles(self.tile.rules[DOWN], from_dir=UP)

        if self.position[0] > 0:
            neighbour_right = cells[self.position[0]][self.position[1] - 1]
            neighbour_right.update_possible_tiles(self.tile.rules[UP], from_dir=DOWN)

    def display(self, window: pg.Surface):
        if self.collapsed:
            window.blit(self.tile.base_image, (self.position[0] * self.size, self.position[1] * self.size))
        elif SHOW_ENTROPY:
            text = pg.font.SysFont("Arial", 10).render(str(self.entropy), True, (255, 255, 255))
            window.blit(text, (self.position[0] * self.size, self.position[1] * self.size))
            # for index, tile in enumerate(self.possibilities):
            #     window.blit(pg.transform.scale(tile.base_image, (10, 10)), (self.position[0] * self.size, self.position[1] * self.size  + (index * 10)))
            #     text = pg.font.SysFont("Arial", 10).render(str(tile.rules), True, (255, 255, 255))
            #     window.blit(text, (self.position[0] * self.size + 10, self.position[1] * self.size + (index * 10)))

    def __repr__(self):
        return f"Cell({self.position}, {len(self.possibilities)})"

cells = [[Cell((x, y)) for y in range(DIM)] for x in range(DIM)]


def get_min_entropy_cell(cells: list):
    # if multiple cells have the same entropy, get a random one
    cells = [[cell for cell in row if not cell.collapsed] for row in cells]
    random.shuffle(cells)
    return min([cell for row in cells for cell in row if not cell.collapsed], key=lambda cell: cell.entropy)


def grid_collapsed(cells: list):
    return all([cell.collapsed for row in cells for cell in row])


def collapse_initial(cells: list):
    position = (random.randint(0, DIM - 1), random.randint(0, DIM - 1))
    cells[position[0]][position[1]].collapse()
    cells[position[0]][position[1]].update_neighbours(cells)

collapse_initial(cells)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            cells = [[Cell((x, y)) for y in range(DIM)] for x in range(DIM)]
            collapse_initial(cells)
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFTBRACKET:
            if SPEED > 1:
                SPEED -= 1
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHTBRACKET:
            if SPEED < 10:
                SPEED += 1

    # for row in cells:
    #     for cell in row:
    #         print(cell, end=" ")
    #     print()

    if not grid_collapsed(cells):
        current_cell = get_min_entropy_cell(cells)
        current_cell.collapse()
        current_cell.update_neighbours(cells)

    window.fill((0, 0, 0))
    for row in cells:
        for cell in row:
            cell.display(window)
    pg.display.update()
    if SPEED < 10:
        time.sleep(1 / (SPEED * 100))
