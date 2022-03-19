from collections import defaultdict

import numpy as np
import time
import random
import copy

######################SUDOKU ENVIRONMENT BELOW##############################
class SudokuEnv:
    """Sudoku environment from which all constraint satisfaction happens."""
    
    def __init__( self, puzzle : np.ndarray ):
        self.row, self.col = puzzle.shape
        
        # init final values
        self.final_values = [0] * self.row * self.col

        # create the Sudoku table as a dictionary, update values with current Sudoku table values if present
        self.possible_values = defaultdict()
        for (y,x), value in np.ndenumerate(puzzle):
            index = y * self.row + x
            self.possible_values[index] = [] if value != 0 else list(range(1, self.row+1))
            if value != 0: self.final_values[index] = value

        # after dict is created, delete all the rcbs for values already placed in final_values list
        [self.__eliminate_rcb( index = key ) for key, values in self.possible_values.items() if len(values) <= 1]

    def __plus_minus( self ):
        """Flip between +1 and -1 for iterating through Sudoku box dict."""
        while True:
            yield 0
            yield 1
            yield -1

    def __eliminate_rcb( self, index : int):
        """Eliminate the rows, cols, boxes with reocurring values."""
        value = self.final_values[index]    # look at what value is at passed index (must be x1!)
        
        if value != 0:
            colloc = (index % self.col)
            rowloc = index // self.row

            # set cell with number being added in to have zero remaining options
            self.possible_values[ index ] = []

            # eliminate value from columns and rows and boxes
            row_shift = -(self.row) * (1 + (rowloc % 3))
            flip = self.__plus_minus()
            for i in range( self.col ):
                # eliminate values from cols
                col_index = index - colloc + i
                if value in self.possible_values[ col_index ] and len(self.possible_values[ col_index ]) >= 1:
                    self.possible_values[ col_index ].remove(value)

                # eliminate values from rows
                row_index = index - (self.row * rowloc) + (self.row * i)
                if value in self.possible_values[ row_index ] and len(self.possible_values[ row_index ]) >= 1:
                    self.possible_values[ row_index ].remove(value)

                # eliminate values from boxes
                if i % 3 == 0:
                    row_shift += self.row
                if colloc % 3 == 0: # zeroth col
                    # (i % 3) --> +0, +1, +2
                    col_shift = (i % 3)
                elif colloc % 3 == 1: # first col
                    # flip.plus_minus() --> +0, +1, -1
                    col_shift = next(flip)
                elif colloc % 3 == 2: # second col
                    # -(i % 3) --> -0, -1, -2
                    col_shift = -(i % 3)
                else:
                    raise ValueError("[INFO]: Box shifting not working as expected!")

                box_index = index + col_shift + row_shift
                if value in self.possible_values[ box_index ] and len(self.possible_values[ box_index ]) >= 1:
                    self.possible_values[ box_index ].remove(value)

    def is_goal( self ):
        """Goal state reached if every value is not equal to zero."""
        return True if 0 not in self.final_values else False

    def is_legal(self):
        """This state is illegal if cells no longer have possible values and are still empty."""
        for key, value in self.possible_values.items():
            if self.final_values[ key ] == 0 and len( value ) < 1: return False
        return True

    def get_possible_values( self ):
        """Return the possible values for a specifc index."""
        return self.possible_values

    def __set_singleton_cells( self ):
        """Writes values to cells which have exactly 1 possible value."""
        for key, value in self.possible_values.items():
            if self.final_values[ key ] == 0 and len( value ) == 1: 
                self.final_values[ key ] = value[0]
                self.__eliminate_rcb( key )

    def assign_value( self, index, value ):
        """Based on CSP approach, search algorithm has decided to try a value, now do it!"""
        if index in self.possible_values:   # check if legal
            if value in self.possible_values[ index ]: 
            
                # deep copy of child state (not overwriting existing data in state)
                child_state = copy.deepcopy( self )

                child_state.final_values[ index ] = value    # assign new value

                child_state.__eliminate_rcb( index )  # constraint satisfaction propagation

                child_state.__set_singleton_cells()   # set singletons created after eliminate_rcb funct call

                return child_state

            else: raise ValueError("[INFO]: Value not in possible_values at index!")
        else: raise ValueError("[INFO]: Index does not exist in possible_values dict!")

    def __str__( self ):
        """Return a string Sudoku matrix for debugging."""
        d2array = [self.final_values[i:i + self.col] for i in range(0, len(self.final_values), self.col)]
        return f"{np.matrix( d2array )}"


######################SEARCHING ALGORITHM BELOW##############################

def check_sudoku( grid ):
    """ Return True if grid is a valid Sudoku square, otherwise False. """
    # convert to numpy array if not already converted
    grid = np.array(grid) if not isinstance(grid,np.ndarray) else grid

    for i in range(9):
        # j, k index top left hand corner of each 3x3 tile
        j, k = (i // 3) * 3, (i % 3) * 3
        if len(set(grid[i,:])) != 9 or len(set(grid[:,i])) != 9\
                        or len(set(grid[j:j+3, k:k+3].ravel())) != 9:
            return False
    return True

def pick_next_cell( state ):
    """
    Used in depth first search, currently chooses a random 
    column that has more than one possible value
    """
    
    cell_indices = [ keys for keys, values in state.possible_values.items() if len(values) > 0 ]
    # return random.choice( cell_indices )

    min = 10
    min_index = None
    for index in cell_indices:
        val = len(state.possible_values[index])
        if len(state.possible_values[index]) < min:
            min = val
            min_index = index
    return min_index

def order_possible_values( state, index ):
    """
    Get values for a particular column in the 
    order we should try them in. Currently random.
    """
    values = state.possible_values[ index ]
    random.shuffle(values)
    return values

def depth_first_search( state ):
    """
    This will do a depth first search on partial states, trying 
    each possible value for a single column.

    Notice that we do not need to try every column: if we try 
    every possible value for a column and can't find a
    solution, then there is no possible value for this column, 
    so there is no solution.
    """
    index = pick_next_cell( state )
    values = order_possible_values( state, index)

    for value in values:
        new_state = state.assign_value( index, value )

        if new_state.is_goal():
            return new_state

        if new_state.is_legal():
            deep_state = depth_first_search( new_state )

            if deep_state is not None and deep_state.is_goal():
                return deep_state
   
    return None


def sudoku_solver( puzzle : np.array ):

    # if check_sudoku( puzzle ):
    final = depth_first_search( SudokuEnv( puzzle ) )

    if final is not None:
        result = np.array( [final.final_values[i:i + final.col] for i in range(0, len(final.final_values), final.col)] )
        return result
    return -np.ones((9, 9))



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




# if __name__ == '__main__':
#     puzzle = [[5,1,2,6,7,4,8,3,0],
#             [6,0,0,1,9,5,0,0,0],
#             [0,9,8,0,0,0,0,6,0],
#             [8,0,0,0,6,0,0,0,3],
#             [4,0,0,8,0,3,0,0,1],
#             [7,0,0,0,2,0,0,0,6],
#             [0,6,0,0,0,0,2,8,0],
#             [0,0,0,4,1,0,0,0,5],
#             [0,0,0,0,8,0,0,7,0]]

#     puzzle=[[5,3,0,0,7,0,0,0,0],
#             [6,0,0,1,9,5,0,0,0],
#             [0,9,8,0,0,0,0,6,0],
#             [8,0,0,0,6,0,0,0,3],
#             [4,0,0,8,0,3,0,0,1],
#             [7,0,0,0,2,0,0,0,6],
#             [0,6,0,0,0,0,2,8,0],
#             [0,0,0,4,1,9,0,0,5],
#             [0,0,0,0,8,0,0,7,9]]

#     # puzzle = np.array(puzzle)

#     difficulties = ['very_easy', 'easy', 'medium', 'hard']
#     difficulty = difficulties[2]
#     sudokus = np.load(f"data/{difficulty}_puzzle.npy")
#     solutions = np.load(f"data/{difficulty}_solution.npy")


#     num = 9
#     puzzle = sudokus[num]

#     # print(f"Problem:\n{sudokus[num]}")
#     # print("")
#     # print(f"Solution:\n{solutions[num]}")

#     env = SudokuEnv(puzzle)

#     # env.__eliminate_rcb(index = 2)

#     # depth_first_search( env )

#     sudoku_solver( puzzle )

#     # print(f"Answer:\n{depth_first_search( env )}")


#     # print(f"{env} \n")
#     # child_env = env.assign_value( value = 2, index = 8 )
#     # print(f"{child_env} \n")
#     # print(f"{env} \n")

#     # pick_next_cell(env)

#     # print(f"Is Legal: {env.is_legal()}")
#     # print(f"Is Goal: {env.is_goal()}")



    

#     # # child_env.change_things()
#     # print(env.possible_values)