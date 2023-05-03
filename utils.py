import random
from constants import DIM


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
