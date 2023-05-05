import time
import random
import glob
import pygame as pg

from tile import Tile
from cell import Cell
from utils import collapse_initial, grid_collapsed, get_min_entropy_cell
from constants import (
    DIM,
    SHOW_ENTROPY,
    SPEED,
    STEP_BY_STEP,
    window,
    empty_image,
)

tiles = [
    Tile(empty_image, 0, [0, 0, 0, 0])
]
for tile in glob.glob("tiles/smallerboard/*.png"):
    for rot in range(4):
        tiles.append(Tile(pg.image.load(tile), rot, infer_from_image=True))

# for tile in glob.glob("tiles/9x9/*.png"):
#     for rot in range(4):
#         tiles.append(Tile(pg.image.load(tile), rot, infer_from_image=True))

cells = [[Cell((x, y), tiles=tiles) for y in range(DIM)] for x in range(DIM)]

collapse_initial(cells)

step = False
stopped = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            stopped = False
            cells = [[Cell((x, y), tiles=tiles) for y in range(DIM)] for x in range(DIM)]
            collapse_initial(cells)
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFTBRACKET:
            if SPEED > 1:
                SPEED -= 1
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHTBRACKET:
            if SPEED < 10:
                SPEED += 1
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            step = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            SHOW_ENTROPY = not SHOW_ENTROPY

    if not STEP_BY_STEP:
        step = True

    if not grid_collapsed(cells) and step and not stopped:
        step = False
        if SHOW_ENTROPY:
            for row in cells:
                for cell in row:
                    print("%02d" % cell.entropy, end=" ")
                print()
            print("-" * 20)

        current_cell = get_min_entropy_cell(cells)
        if current_cell.entropy == 0:
            print("No solution found")
            stopped = True
        else:
            current_cell.collapse()
            current_cell.update_neighbours(cells)

    window.fill((0, 0, 0))
    for row in cells:
        for cell in row:
            cell.display(window)
    pg.display.update()
    if SPEED < 10:
        time.sleep(1 / (SPEED * 100))
