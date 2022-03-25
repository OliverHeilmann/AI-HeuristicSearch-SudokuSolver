# By Oliver Heilmann
# Date: 25/03/2022

from tests import run_tests

import numpy as np
import copy
import time

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
    global is_solved

    def possible(y,x,n):
        for i in range(0,9):
            if grid[y][i] == n or grid[i][x] == n:
                return False

        x0 = (x//3)*3
        y0 = (y//3)*3

        for i in range(0,3):
            for j in range(0,3):
                if grid[y0+i][x0+j]==n:
                    return False
        return True

    def solve():
        global is_solved, solution
        if is_solved:
            return True

        for y in range(0,9):

            for x in range(0,9):

                if grid[y][x] == 0:

                    for n in range(1,10):
                        if possible(y,x,n):
                            grid[y][x] = n
                            solve()
                            grid[y][x] = 0
                    return False
        
        # print(f"Solution!\n{np.matrix(grid)}")
        if solve.store == None:
            solve.store = copy.deepcopy(np.array(grid))
        is_solved = True

    is_solved = False
    solve.store = None
    solve()

    if solve.store is not None:
        if check_sudoku(solve.store):
            return solve.store
    else:
        return not_solvable


# V Hard Puzzle
puzzle = [[0,6,1,0,0,7,0,0,3],
          [0,9,2,0,0,3,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,8,5,3,0,0,0,0],
          [0,0,0,0,0,0,5,0,4],
          [5,0,0,0,0,8,0,0,0],
          [0,4,0,0,0,0,0,0,1],
          [0,0,0,1,6,0,8,0,0],
          [6,0,0,0,0,0,0,0,0]]

if __name__ == "__main__":
    # pass the solver through to run tests on it
    run_tests( sudoku_solver, skip_tests=False) #, puzzle=np.array(puzzle))