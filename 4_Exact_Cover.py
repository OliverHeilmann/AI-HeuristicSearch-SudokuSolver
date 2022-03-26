# By Oliver Heilmann
# Date: 25/03/2022

# creating new branch for improving exact cover

from collections import defaultdict
from collections import Counter
from tests import run_tests, create_puzzle
from itertools import product

import numpy as np
import _pickle as cPickle
import time
import random
import copy

###################### SUDOKU ENVIRONMENT BELOW ##############################
class SudokuEnv:
    """Sudoku environment from which all constraint satisfaction happens."""
    def __init__( self, grid : np.ndarray ):
        (row, self.col) = grid.shape

        # init final values np array (could deepcopy grid but will be looping through below anyway)
        self.result = np.array( [[0] * row] * self.col )

        self.R = dict()
        self.C = defaultdict( lambda : set() )  # dynamically create set when key is made

        # Make both column and R in same loop -> colverCols will have 
        # cases where items are overwritten but not an issue at initialisation.
        for r, c, val in product( range(row), range(row), range(1,row+1) ):

            # build up results np array
            self.result[r][c] = grid[r][c]

            # Box index as [0, 1, 2, 3, 4 ---> 8] (note only works for 9x9 Sudoku!)
            b = (r//3) * 3 + (c//3)

            # create exact cover R
            self.R[ (r, c, val) ] = [  ("Cell", (r, c)),
                                        ("RowN", (r, val)),    # +1 to val for range 1->9
                                        ("ColN", (c, val)),    # +1 to val for range 1->9
                                        ("BoxN", (b, val))]    # +1 to val for range 1->9

            # create exact cover column dictionary if not already made, then add constraint 
            # to it immediately (if not already present)
            self.C[ "Cell", (r, c) ].add( (r, c, val) )
            self.C[ "RowN", (r, val) ].add( (r, c, val) )
            self.C[ "ColN", (c, val) ].add( (r, c, val) )
            self.C[ "BoxN", (b, val) ].add( (r, c, val) )

        # loop through grid and delete rcv's which conflict with pre-assigned grid vals
        # ( no need to store these as the values are already fixed on Sudoku grid )
        for (r, c), val in np.ndenumerate( grid ):
            if val: self.__eliminateRCV( (r, c, val) )

    def is_goal( self ):
        """Goal state reached if every value is not equal to zero."""
        return True if 0 not in self.result else False

    def __eliminateRCV( self, RCV ):
        """Delete all conflicting rcv's, but store them in a returned list.'"""
        rcvStore = list()
        for c in self.R[ RCV ]:   # for all the cols at current row
            for _rcv in self.C[ c ]: # for all the rcvs at current col (col and row now)
                for _c in self.R[ _rcv ]: # for the col entries at current row
                    if _c != c: self.C[ _c ].remove( _rcv )
            rcvStore.append( self.C.pop( c ) )
        return rcvStore

    def __restoreRCV( self, RCV, rcvStore ):
        """Restore the deleted rcv's that were passed as a list (opposite of eliminate method)."""
        for c in self.R[ RCV ][::-1]:
            self.R[ c ] = rcvStore.pop()    # does this need to be reversed?
            for _rcv in self.C[ c ]:
                for _c in self.R[ _rcv ]:
                    if _c != c: self.C[ _c ].add( _rcv )

    def assign_value( self, rcv ):
        """Assign value to Sudoku results array and eliminate option from """

        # child_state = cPickle.loads( cPickle.dumps(self, -1) )
        child_state = copy.deepcopy( self )

        ( r, c, v ) = rcv
        child_state.result[ r ][ c ] = v  # add entry to results array

        child_state.__eliminateRCV( rcv )
        return child_state

    def __str__( self ):
        """Return a string Sudoku matrix for debugging."""
        return f"{self.result}"


###################### SEARCHING ALGORITHM BELOW ##############################
def depth_first_search( state ):
    """Use backtracking search approach with constraint satisfaction propagation."""

    c = min( state.C, key=lambda c: len(state.C[c]) ) # pick most constrained column

    for rcv in list( state.C[c] ):

        new_state = state.assign_value( rcv )

        if new_state.is_goal():
            return new_state

        deep_state = depth_first_search( new_state )

        if deep_state is not None and deep_state.is_goal():
            return deep_state

    return None

def sudoku_solver( puzzle : np.array ):
    """Function to conform with coursework framework"""
    
    state = depth_first_search( SudokuEnv( puzzle ) )

    if depth_first_search( SudokuEnv( puzzle ) ) is not None:
        # convert result into a numpy array format
        return state.result

    return -np.ones((9, 9))



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
    env = SudokuEnv( grid=np.array(puzzle) )

    run_tests( sudoku_solver, skip_tests=False) #, puzzle=np.array(puzzle))