from collections import defaultdict

# Helper functions
from grid import grid_num, rc2cell, cell2rc
from config import GRID_SIZE, V, board_config, board_constraints

# Graph implementation details
from sudoku_graph import Graph, get_graph

import time

hm_row = defaultdict(set)
hm_col = defaultdict(set)
hm_grid = defaultdict(set)

total_moves = 0
total_backtracks = 0


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

def is_valid(board, row, col, num, board_graph=None):
    """ Checks whether it is valid to have num in board[row][col] """

    # Check that coordinate is empty
    if board[row][col] != 0:
        return False

    if (num in hm_row[row]) or (num in hm_col[col]):
        return False

    grid = grid_num(row, col)
    if num in hm_grid[grid]:
        return False
    
    # Check connected component constraint
    if board_graph is None:
        return True  # Has to be True if no board_graph (Kill Sudoku) since all constraints were already checked
    else:
        # Obtain list of all nodes in connected component
        for component_num in range(len(board_graph.cc)):
            connected_nodes = board_graph.cc[component_num]
            cell = rc2cell(row, col)
            if cell in connected_nodes:
                break

        # As long as one of the cells is still 0, we return True first
        # TODO Can be optimised to skip numbers we know definitely will no longer work?
        current_sum = 0
        for cell in connected_nodes:
            r,c = cell2rc(cell)
            if (r,c) == (row,col):
                current_sum += num # Current number being evaluated
            elif board[r][c] == 0:
                return True
            else:
                current_sum += board[r][c]

        if current_sum == board_graph.constraints[component_num]:
            # print(f'Matched component {component_num} with sum of {current_sum}')
            return True
        else:
            return False


def get_next_cell(board):
    """ Returns the next available cell - returns None, None if no more valid cells (meaning we have solved it) """

    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                return r, c

    return None, None

def solve(board, board_graph):
    """ Recursive function to solve the board """

    global total_moves, total_backtracks

    # Get next valid cell
    row, col = get_next_cell(board)
    print(f'Solving [{row}:{col}]')
    
    # Base case - we have no more unfilled cells.  Solved!
    if row == col == None:
        return True

    for guess in range(1,10):
        if is_valid(board, row, col, guess, board_graph):
            total_moves += 1

            board[row][col] = guess
            
            from contextlib import redirect_stdout
            with open('solution.log', 'a') as f:
                with redirect_stdout(f):
                    print_board(board)
                    print()
            
            # Update the hash map
            grid = grid_num(row, col)
            hm_row[row].add(guess)
            hm_col[col].add(guess)
            hm_grid[grid].add(guess)

            # Recurse
            if not solve(board, board_graph):  # Wrong guess - backtrack
                total_backtracks += 1
                hm_grid[grid].remove(guess)
                hm_col[col].remove(guess)
                hm_row[row].remove(guess)
                board[row][col] = 0
            else:
                return True

    return False

if __name__ == '__main__':

    start_time = time.time()
    board_graph = get_graph(board_config, board_constraints)
    # board_graph.print_graph()

    # Initialises the empty board
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    hm_row, hm_col, hm_grid = init_hash_map(board)

    if solve(board, board_graph):
        end_time = time.time()
        print(f'Solved in {total_moves} steps, backtracking {total_backtracks} times')
        print(f'Total time taken: {end_time-start_time} seconds')
        print_board(board)
    else:
        end_time = time.time()
        print('No solutions found')
        print(f'Total time taken: {end_time-start_time} seconds')
        print_board(board)
