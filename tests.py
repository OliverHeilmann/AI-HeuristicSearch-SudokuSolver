import numpy as np
import time

def create_puzzle():
    """Create puzzle of random complexity. Use for testing solver robustness only."""
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


def run_tests( sudoku_solver , skip_tests : bool = False, puzzle=None):

    ST = time.process_time()

    if not skip_tests:
        if puzzle is not None:
            your_solution = sudoku_solver(puzzle)
        else:
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
        
    ET = time.process_time()
    print(f"--> TOTAL TIME: {(ET-ST)*1000}ms\n")