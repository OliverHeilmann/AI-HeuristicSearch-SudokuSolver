import numpy as np
import time

# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")




def solve_sudoku(grid):
    '''
    0: represents empty squares
    1-9: numbers used by sudoku
    arrays indexed by n-1 (ie number 5 is index 4)
    '''
    
    
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

    backtrack()

    return grid


numbers = sudoku[-1]
print(f'Problem:\n{numbers}')
nums = solve_sudoku(numbers)
print(f'Solution:\n{nums}')


