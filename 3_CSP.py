# Written by Oliver Heilmann
# For performance testing, use:
#   scalene --profile-interval 5.0 CODENAME.py
#
# (Note: Convert to cython for faster performance!)

from collections import defaultdict
from collections import Counter
from tests import run_tests, create_puzzle

import numpy as np
import _pickle as cPickle
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

    def get_counts( self ):
        """Return the counts of each number in Sudoku puzzle (excluding zeros)"""
        counts = Counter( self.final_values )
        del counts[0]

        # add 1 -> 9 if not already in (where puzzle doesn't have any X's on the board)
        for i in range( 1, self.row+1 ):
            if i not in counts: counts[i] = 0
        return counts
        
    @classmethod
    def __plus_minus( cls ):
        """Flip between +1 and -1 for iterating through Sudoku box dict."""
        while True:
            yield 0
            yield 1
            yield -1

    def __eliminate_rcb( self, index : int):
        """Eliminate the rows, cols, boxes with reocurring values."""
        value = self.final_values[ index ]    # look at what value is at passed index (must be x1!)
        
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

    def is_legal( self ):
        """This state is illegal if cells no longer have possible values and are still empty."""
        for key, value in self.possible_values.items():
            if self.final_values[ key ] == 0 and len( value ) < 1: return False
        return True

    def __set_singleton_cells( self ):
        """Writes values to cells which have exactly 1 possible value."""
        items = [-1]
        while any( items ): # after adding new singletons, sometimes more appear, while loop to catch them!
            items = [ (key,value) for key, value in self.possible_values.items() if len( value ) == 1 ]
            for key, value in items:
                if self.final_values[ key ] == 0 and len( value ) == 1: 
                    self.final_values[ key ] = value[0]
                    self.__eliminate_rcb( index = key )

    def assign_value( self, index, value ):
        """Based on CSP approach, search algorithm has decided to try a value, now do it!"""
        if index in self.possible_values:   # check if legal
            if value in self.possible_values[ index ]: 
            
                # deep copy of child state (not overwriting existing data in state)
                # child_state = copy.deepcopy( self )
                child_state = cPickle.loads( cPickle.dumps(self, -1) )  # method reduces time taken by x1 second

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

    # def __deepcopy__( self, memodict={} ):
    #     """Custom Deepcopy to avoid uneccessary copying of object atributes (speed up code)."""
    #     cls = self.__class__
    #     state = cls.__new__( cls )
    #     state.final_values = copy.deepcopy(self.final_values)#.copy()
    #     state.possible_values = copy.deepcopy(self.possible_values)#.copy()
    #     state.row, state.col = (self.row, self.col)
    #     return state


#########################SUDOKU CHECKER BELOW#################################
def check_sudoku( grid ):
    """ Return True if grid is a valid Sudoku puzzle else False."""
    # convert to numpy array if not already converted
    grid = np.array(grid) if not isinstance(grid,np.ndarray) else grid

    for i in range( grid.shape[0] ):
        # j, k index top left hand corner of each 3x3 tile
        j, k = (i // 3) * 3, (i % 3) * 3

        # row excluding zeros
        row = grid[i,:][ grid[i,:] != 0 ]
        row_repeated = len( set(np.unique(row, return_counts=True)[1]) ) > 1

        # col excluding zeros
        col = grid[:,i][ grid[:,i] != 0 ]
        col_repeated = len( set(np.unique(col, return_counts=True)[1]) ) > 1

        # box excluding zeros
        box = grid[j:j+3, k:k+3][ grid[j:j+3, k:k+3] != 0 ]
        box_repeated = len( set(np.unique(box, return_counts=True)[1]) ) > 1

        if row_repeated or col_repeated or box_repeated: return False
    return True


######################SEARCHING ALGORITHM BELOW##############################
def pick_next_cell( state ):
    """Return the index of the most constrained cell next."""
    vals = [ value for index, value in state.possible_values.items() if len(value) > 0 ]
    min_index = list( state.possible_values.values() ).index( min(vals, key=len) )
    return min_index

def order_possible_values( state, index ):
    """Order the values so most constraining value (value placed most frequently) is chosen."""
    possVals = state.possible_values[ index ]
    values = [ num[0] for num in reversed(state.get_counts().most_common()) if num[0] in possVals ]
    return values

def depth_first_search( state ):
    """Use backtracking search approach with constraint satisfaction propagation."""
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
    """Function to conform with coursework framework"""
    if check_sudoku( puzzle ):
        final = depth_first_search( SudokuEnv( puzzle ) )

        if final is not None:
            # convert result into a numpy array format
            result = np.array( [final.final_values[i:i + final.col] for i in range(0, len(final.final_values), final.col)] )
            return result
    return -np.ones((9, 9))


######################PERFORMANCE TESTS BELOW##############################
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

    for i in range(1000):
        puzzle = create_puzzle()
        ST = time.process_time()
        sudoku_solver( puzzle )
        ET = time.process_time()
        if ET-ST > 10:
            print(puzzle)
            print(f"Puzzle {i} | Time: {ET-ST}")

    # run_tests( sudoku_solver, skip_tests=False) #, puzzle=np.array(puzzle))