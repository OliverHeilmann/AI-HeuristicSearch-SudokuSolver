import numpy as np
import time
import csv, random

def create_puzzle():
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board =[ [nums[pattern(r,c)] for c in cols] for r in rows ]

    squares = side*side
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        board[p//side][p%side] = 0

    return np.array(board)


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
    '''
    0: represents empty squares
    1-9: numbers used by sudoku
    arrays indexed by n-1 (ie number 5 is index 4)
    '''
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
    



puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]


puzzle = [[0,6,1,0,0,7,0,0,3],
          [0,9,2,0,0,3,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,8,5,3,0,0,0,0],
          [0,0,0,0,0,0,5,0,4],
          [5,0,0,0,0,8,0,0,0],
          [0,4,0,0,0,0,0,0,1],
          [0,0,0,1,6,0,8,0,0],
          [6,0,0,0,0,0,0,0,0]]

# if __name__ == '__main__':
    # print("Running...")
    # start_time = time.process_time()
    # sudoku_solver(puzzle)
    # end_time = time.process_time()
    # total_time = end_time-start_time
    # print(f"Total Time: {total_time}s")

    
    # start_time = time.process_time()
    # num = 100
    # for i in range(num):
    #     if i % 1 == 0:
    #         print(f"Step {i}...")
    #     puzzle = create_puzzle()
    #     sudoku_solver(puzzle)

    # end_time = time.process_time()
    # total_time = end_time-start_time

    # with open('times.csv','a') as fd:
    #     writer = csv.writer(fd)
    #     writer.writerow([total_time])

    # print(f"Puzzles Solved: {num}\nTotal Time: {total_time}s")



if __name__ == "__main__":
    SKIP_TESTS = False

    if not SKIP_TESTS:
        difficulties = ['very_easy', 'easy', 'medium', 'hard']

        for difficulty in difficulties:
            print(f"Testing {difficulty} sudokus")

            sudokus = np.load(f"data/{difficulty}_puzzle.npy")
            solutions = np.load(f"data/{difficulty}_solution.npy")

            count = 0
            for i in range(len(sudokus)):
                sudoku = sudokus[i].copy()
                print(f"This is {difficulty} sudoku number", i)
                print(sudoku)

                start_time = time.process_time()
                your_solution = sudoku_solver(sudoku)
                end_time = time.process_time()

                print(f"This is your solution for {difficulty} sudoku number", i)
                print(your_solution)

                print("Is your solution correct?")
                if np.array_equal(your_solution, solutions[i]):
                    print("Yes! Correct solution.")
                    count += 1
                else:
                    print("No, the correct solution is:")
                    print(solutions[i])

                print("This sudoku took", end_time - start_time, "seconds to solve.\n")

            print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
            if count < len(sudokus):
                break