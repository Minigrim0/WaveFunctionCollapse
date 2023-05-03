import pygame as pg

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIM = 20
SIZE = 20
SHOW_ENTROPY = False
SPEED = 10
STEP_BY_STEP = False


pg.init()
window = pg.display.set_mode((400, 400))

empty_image = pg.Surface((SIZE, SIZE))
empty_image.fill((255, 255, 255))

error_image = pg.Surface((SIZE, SIZE))
error_image.fill((255, 0, 0))
