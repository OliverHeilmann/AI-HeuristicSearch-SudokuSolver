# Code modified by Oliver Heilmann
# Date: 25/03/2022
#
# Original author is Tech Tribe and the Github link can be found at:
#       --> https://github.com/techtribeyt/sudoku

from tests import run_tests, create_puzzle

import numpy as np
import time
import csv, random


not_solvable = -np.ones((9, 9))

def check_sudoku(grid):
    """ Return True if grid is a valid Sudoku square, otherwise False. """
    # convert to numpy array if not already converted
    grid = np.array(grid) if not isinstance(grid,np.ndarray) else grid

    if any(np.concatenate((np.where(grid==0)), axis=0)):
        return False

    for i in range(9):
        # j, k index top left hand corner of each 3x3 tile
        j, k = (i // 3) * 3, (i % 3) * 3
        if len(set(grid[i,:])) != 9 or len(set(grid[:,i])) != 9\
                        or len(set(grid[j:j+3, k:k+3].ravel())) != 9:
            return False
    return True

def sudoku_solver(grid):
    """Main backtracking solver."""
    # if check_sudoku(grid):
    # define 2D arrays to keep track whether each row/col/region needs number
    row = [[True] * 9 for i in range(9)]
    col = [[True] * 9 for i in range(9)]
    regions = [[True] * 9 for i in range(9)]

    # list of tuples containing coordinates of empty locations
    to_add = []

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # mark row/col/region as False, meaning we don't need that number anymore
                d = grid[i][j] - 1
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = False
            else:
                # need to find number of this spot
                to_add.append((i, j))

  
    def backtrack():
        backtrack.counter +=1

        if not to_add:
            # all squares full - we did it!
            return True
        
        # get next empty square
        i, j = to_add.pop()
        for d in range(9):
            # if number d can be legally inserted
            if row[i][d] and col[j][d] and regions[i // 3 * 3 + j // 3][d]:
                grid[i][j] = d + 1
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = False
                
                # try next empty spot
                if backtrack():
                    # success!
                    return True
                
                # backtrack failed, so reset and try next number
                grid[i][j] = 0
                row[i][d] = col[j][d] = regions[i // 3 * 3 + j // 3][d] = True
                
        # found no legal move - something went wrong in previous iterations!
        to_add.append((i, j))
        return False

    backtrack.counter = 0
    backtrack()
    print(f"Nodes Explored: {backtrack.counter}")
    
    if check_sudoku(grid):
        return np.array(grid)
    else:
        return not_solvable


# World's Hardest Puzzle
puzzle = [[8,0,0,0,0,0,0,0,0],
          [0,0,3,6,0,0,0,0,0],
          [0,7,0,0,9,0,2,0,0],
          [0,5,0,0,0,7,0,0,0],
          [0,0,0,0,4,5,7,0,0],
          [0,0,0,1,0,0,0,3,0],
          [0,0,1,0,0,0,0,6,8],
          [0,0,8,5,0,0,0,1,0],
          [0,9,0,0,0,0,4,0,0]]

if __name__ == "__main__":
    # pass the solver through to run tests on it
    run_tests( sudoku_solver, skip_tests=False) #, puzzle=puzzle )

    # for i in range(100):
    #     puzzle = create_puzzle()
    #     run_tests( sudoku_solver, skip_tests=False, puzzle=puzzle )