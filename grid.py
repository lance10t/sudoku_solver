def grid_num(row, col):
    """ Returns the 3x3 grid number - 0-indexed """
    return ((row // 3) * 3) + (col // 3)

def rc2cell(row, col, grid_size=9):
    """ Returns the cell number if the board was a contiguous array.
    Assumes a 0-indexed array, and 9x9 grid """
    return (row * grid_size) + col

def cell2rc(cell, grid_size=9):
    """ Returns the row, cell coordinates from a cell number.
    Assumes a 0-indexed array, and 9x9 grid """
    return (cell // grid_size), (cell % grid_size)