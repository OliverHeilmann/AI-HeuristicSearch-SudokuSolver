import numpy as np
import time
   

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
    print("\nTOTAL TIME:",ET-ST,"s")