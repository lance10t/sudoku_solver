# Defines the grid size, with the assumption that it is a square grid
GRID_SIZE = 9
V = GRID_SIZE ** 2

# This board configuration is supposedly the "World's Hardest Sudoku"
# https://gizmodo.com/can-you-solve-the-10-hardest-logic-puzzles-ever-created-1064112665
board_config = [
    ['AA', 'AA', 'AB', 'AB', 'AC', 'AC', 'AD', 'AD', 'AE'],
    ['AA', 'AF', 'AB', 'AG', 'AC', 'AH', 'AH', 'AD', 'AE'],
    ['AI', 'AF', 'AJ', 'AG', 'AK', 'AK', 'AH', 'AL', 'AE'],
    ['AI', 'AF', 'AJ', 'AJ', 'AK', 'AM', 'AM', 'AL', 'AN'],
    ['AO', 'AP', 'AP', 'AQ', 'AQ', 'AM', 'AR', 'AL', 'AN'],
    ['AO', 'AO', 'AS', 'AQ', 'AT', 'AU', 'AR', 'AV', 'AN'],
    ['AW', 'AW', 'AS', 'AT', 'AT', 'AU', 'AX', 'AV', 'AV'],
    ['AW', 'AW', 'AY', 'AY', 'AY', 'AY', 'AX', 'AV', 'AV'],
    ['AZ', 'AZ', 'AZ', 'AZ', 'AY', 'BA', 'BA', 'BB', 'BB'],
]

board_constraints = {
    'AA': 15,
    'AB': 19,
    'AC': 16,
    'AD': 8,
    'AE': 19,
    'AF': 15,
    'AG': 4,
    'AH': 18,
    'AI': 7,
    'AJ': 16,
    'AK': 16,
    'AL': 12,
    'AM': 17,
    'AN': 17,
    'AO': 17,
    'AP': 10,
    'AQ': 20,
    'AR': 7,
    'AS': 6,
    'AT': 9,
    'AU': 7,
    'AV': 26,
    'AW': 23,
    'AX': 12,
    'AY': 26,
    'AZ': 21,
    'BA': 12,
    'BB': 10,
}