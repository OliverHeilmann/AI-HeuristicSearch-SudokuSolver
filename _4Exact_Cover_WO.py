# By Oliver Heilmann
# Date: 25/03/2022

# Decription:
#   --> Algorithm X is a recursive, nondeterministic, depth-first, backtracking algorithm 
#       that finds all solutions to the exact cover problem. Rather than using the Dancing 
#       Links approach (DLX), this code recursively eliminates and restores dictionary
#       elements. While this is less computationally efficient, the benefits gained from 
#       code simplicity, as well as the performance gain from using mutable data structures
#       (i.e. not deepcopying states), were sufficiently justified. Thank you to A. Assaf 
#       for his description on his alternative Algorithm X implimentation at the following
#       website: https://www.cs.mcgill.ca/~aassaf9/.

from collections import defaultdict
from tests import run_tests, create_puzzle
from itertools import product
import numpy as np

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

    def __eliminateRCV( self, RCV : tuple ):
        """Delete all conflicting rcv's, but store them in a returned list.'"""
        rcvStore = list()
        for c in self.R[ RCV ]:   # for all the cols at current row
            for _rcv in self.C[ c ]: # for all the rcvs at current col (col and row now)
                for _c in self.R[ _rcv ]: # for the col entries at current row
                    if _c != c: self.C[ _c ].remove( _rcv )
            rcvStore.append( self.C.pop( c ) )
        return rcvStore

    def __restoreRCV( self, RCV, rcvStore : list ):
        """Restore the deleted rcv's that were passed as a list (opposite of eliminate method)."""
        for c in self.R[ RCV ][::-1]:
            self.C[ c ] = rcvStore.pop()
            for _rcv in self.C[ c ]:
                for _c in self.R[ _rcv ]:
                    if _c != c: self.C[ _c ].add( _rcv )

    def assign_value( self, RCV : tuple ):
        """Assign value to Sudoku results array and eliminate option."""
        ( r, c, v ) = RCV
        self.result[ r ][ c ] = v  # add entry to results array

        rcvStore = self.__eliminateRCV( RCV )
        return rcvStore

    def unassign_value( self, RCV : tuple, rcvStore : list ):
        """Loop through rcv list and undo previous assignments and restore RCV dict."""
        ( r, c, v ) = RCV
        self.result[ r ][ c ] = 0  # set back to zero

        self.__restoreRCV( RCV, rcvStore )
  
    def __str__( self ):
        """Return a string Sudoku matrix for debugging."""
        return f"{self.result}"


###################### SEARCHING ALGORITHM BELOW ##############################
def backtrack( state : SudokuEnv ):
    """Use backtracking search approach with constraint satisfaction propagation."""
    c = min( state.C, key=lambda c: len(state.C[c]) ) # pick most constrained column

    # loop through rcv's in most constrained column
    for rcv in list( state.C[c] ):
        rcvStore = state.assign_value( rcv )    # assign rcv

        # if goal state or backtrack has returned a valid state, return state again
        if state.is_goal() or backtrack( state ):
            return state

        state.unassign_value( rcv, rcvStore )   # undo the assign if line is reached
    return None

def sudoku_solver( puzzle : np.array ):
    """Function to conform with coursework framework""" 
    state = backtrack( SudokuEnv( puzzle ) )
    return state.result if state is not None else -np.ones((9, 9))


###################### PERFORMANCE TESTS BELOW ##############################
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
    run_tests( sudoku_solver, skip_tests=False) #puzzle=np.array(puzzle))
