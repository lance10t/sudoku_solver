from collections import defaultdict

hm_row = defaultdict(set)
hm_col = defaultdict(set)
hm_grid = defaultdict(set)

total_moves = 0
total_backtracks = 0

# This board configuration is supposedly the "World's Hardest Sudoku"
# https://gizmodo.com/can-you-solve-the-10-hardest-logic-puzzles-ever-created-1064112665
board = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]


def grid_num(row, col):
    """ Returns the 3x3 grid number - 0-indexed """
    return ((row // 3) * 3) + (col // 3)

def init_hash_map(board):
    """ We make use of dictionaries of sets to keep track of the numbers in rows, cols, and grids.
    This makes the search for validity faster than iterating through unnecessarily """

    global hm_row, hm_col, hm_grid

    for r in range(len(board)):
        for c in range(len(board[r])):
            grid = grid_num(r,c)
            hm_row[r].add(board[r][c])
            hm_col[c].add(board[r][c])
            hm_grid[grid].add(board[r][c])
    
    # Remove the empty values - this is technically unnecessary
    for i in range(len(board)):
        hm_row[i].remove(0)
        hm_col[i].remove(0)
        hm_grid[i].remove(0)
    
    return hm_row, hm_col, hm_grid

def print_board(board):
    """ Prints the board """
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f' {board[i][j]} ', end='')
        print()

def is_valid(board, row, col, num):
    """ Checks whether it is valid to have num in board[row][col] """

    # Check that coordinate is empty
    if board[row][col] != 0:
        return False

    if (num in hm_row[row]) or (num in hm_col[col]):
        return False

    grid = grid_num(row, col)
    return num not in hm_grid[grid]

def get_next_cell(board):
    """ Returns the next available cell - returns None, None if no more valid cells (meaning we have solved it) """

    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                return r, c

    return None, None

def solve(board):
    """ Recursive function to solve the board """

    global total_moves, total_backtracks

    # Get next valid cell
    row, col = get_next_cell(board)
    
    # Base case - we have no more unfilled cells.  Solved!
    if row == col == None:
        return True

    for guess in range(1,10):
        if is_valid(board, row, col, guess):
            total_moves += 1

            board[row][col] = guess
            
            # Update the hash map
            grid = grid_num(row, col)
            hm_row[row].add(guess)
            hm_col[col].add(guess)
            hm_grid[grid].add(guess)

            # Recurse
            if not solve(board):  # Wrong guess - backtrack
                total_backtracks += 1
                hm_grid[grid].remove(guess)
                hm_col[col].remove(guess)
                hm_row[row].remove(guess)
                board[row][col] = 0
            else:
                return True

    return False

if __name__ == '__main__':
    # print_board(board)
    hm_row, hm_col, hm_grid = init_hash_map(board)
    # print(is_valid(board, 0, 0, 5))

    if solve(board):
        print(f'Solved in {total_moves} steps, backtracking {total_backtracks} times')
        print_board(board)
    else:
        print('No solutions found')
        print_board(board)
