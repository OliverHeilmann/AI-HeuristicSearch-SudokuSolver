# Solving Sudoku with Heuristic Search
The contents enclosed in this repository explore how backtracking (BT), constraint satisfaction propagation (CSP) and exact cover (EC) algorithm performances differ when solving Sudoku puzzles of varying complexity. For each of these algorithms, various modifications were made to reduce computational time and memory usage; the results of said experiments have been presented and discussed below. 

Overall, the Exact Cover, Algorithm X (without Dancing Links) approach outperformed all other algorithms (on average) and, as such, was selected for submission.

**_(Readers are encouraged to explore the source code for detailed explanation of the algorithms.)_**


## Testing Methods
---
Testing consisted of three main experiments, the coursework specific tests found in the [Jupyter Notebook](sudoku.ipynb), the [world's hardest Sudoku puzzle](https://abcnews.go.com/blogs/headlines/2012/06/can-you-solve-the-hardest-ever-sudoku) and a random puzzle [Sudoku Generator](tests.py). Testing results have been presented first they are referenced frequently in subsequent sections. _Note: Testing hardware is described below._

```text
Hardware Used for Testing:
    MacBook Pro (14-inch, 2021)
    Mac OS Monterey
    Chip: Apple M1 Max
    Memory: 64 GB
```

### Coursework Tests
---
The table below outlines how each algorithm (or variation of) performed on the given coursework tests; relevant scripts can be found in contained in this repository. The fast backtracking algorithm is hyperlinked as the original implementation was found online. During preliminary testing, [_2fastbacktracking.py](_2fastbacktracking.py) was used as a benchmark in determining the "upper limit" of a simple backtracking algorithm performance. The results contained in this table will be discussed in further detail in the following sections.

| Script Name           | **Algorithm**                                           | **Very Easy [ms]** | **Easy [ms]** | **Medium [ms]** | **Hard [ms]** | **Total [ms]** |
|-----------------------|---------------------------------------------------------|--------------------|---------------|-----------------|---------------|----------------|
| [_1backtracking.py](_1backtracking.py)     | Backtracking                                            |         21         |       20      |        47       |     365278    |     365475     |
| [_2fastbacktracking.py](_2fastbacktracking.py) | [Fast Backtracking](https://github.com/techtribeyt/sudoku/blob/main/code.py)     |         13         |       14      |        13       |      6822     |      6768      |
| [_3CSP.py](_3CSP.py)              | Constraint Satisfaction Propagation – Deepcopy          |         37         |       34      |        56       |      3254     |      3411      |
| [_3CSP.py](_3CSP.py)              | Constraint Satisfaction Propagation – cPickle           |         36         |       34      |        56       |      2341     |      2442      |
| [_3CSP.py](_3CSP.py)              | Constraint Satisfaction Propagation – cPickle & Cython  |         35         |       31      |        55       |      1933     |      2046      |
| [_4Exact_Cover_DC.py](_4Exact_Cover_DC.py)   | Exact Cover, Algorithm X (no Dancing Links) – Deepcopy  |         851        |      599      |       2241      |     13324     |      17200     |
| [_4Exact_Cover_WO.py]( _4Exact_Cover_WO.py)   | Exact Cover, Algorithm X (no Dancing Links) – W.O. Copy |         52         |       53      |        55       |       92      |       246      |

### World's Hardest Sudoku Puzzle
---
As the name suggests, the supposed _"world's hardest Sudoku puzzle"_ was used as testing method of benchmarking algorithm performance (measured as total computation time). Testing against the "hardest" puzzle (though hard for a human does not necessarily mean hard for a computer – this will be discussed in following sections) gave some indication as to how each algorithm might perform on the most challenging puzzles in the coursework tests.

```python
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
```

| Script Name                                    | **Algorithm**                                                                 | **Very Hard [ms]** |
|------------------------------------------------|-------------------------------------------------------------------------------|--------------------|
| [_1backtracking.py](_1backtracking.py)         | Backtracking                                                                  |        1915        |
| [_2fastbacktracking.py](_2fastbacktracking.py) | [Fast Backtracking](https://github.com/techtribeyt/sudoku/blob/main/code.py)  |         135        |
| [_3CSP.py](_3CSP.py)                           | Constraint Satisfaction Propagation – Deepcopy                                |          23        |
| [_3CSP.py](_3CSP.py)                           | Constraint Satisfaction Propagation – cPickle                                 |          15        |
| [_3CSP.py](_3CSP.py)                           | Constraint Satisfaction Propagation – cPickle & Cython                        |          10        |
| [_4Exact_Cover_DC.py](_4Exact_Cover_DC.py)     | Exact Cover, Algorithm X (no Dancing Links) – Deepcopy                        |       26369        |
| [_4Exact_Cover_WO.py]( _4Exact_Cover_WO.py)    | Exact Cover, Algorithm X (no Dancing Links) – W.O. Copy                       |          75        |



### Sudoku Generator
---
Depending on the algorithm approach, easy puzzles would often take longer than other, more challenging ones (and vice versa). For the purposes of testing robustness, as well as to determine if the algorithm designs were over fit to the testing puzzles, a random puzzle [Sudoku Generator](tests.py) was used to evaluate the performance of each algorithm. As each test would randomly generate new puzzles, no quantitative data was collected for this test, but rather, a more qualitative approach was adopted (also used for debugging).


## Backtracking
---
### Algorithm Approach
A simple backtracking recursively builds solution candidates and abandons those which are determined as invalid solutions ("backtracks") until a valid solution is reached. While simple to implement, this approach does not scale to larger problems due to the increased complexity of search spaces increasing by the square of the possible states; in the case of Sudoku for example, the maximum search space is 9^9^9, a number far greater than is practical to compute a solution for without some heuristics to further constrain the problem. 

### Backtracking Algorithm
```python
    def solve():
        if is_solved:
            return True

        for y in range(0,9):
            for x in range(0,9):
                if grid[y][x] == 0:
                    for n in range(1,10):
                        if possible(y,x,n): # check if allowable
                            grid[y][x] = n  # set cell to chosen val
                            solve()         # backtrack
                            grid[y][x] = 0  # re-write cell to 0
                    return False
```

### Discussion
Testings results (shown in the tables above) demonstrated that a basic backtracking algorithm worked very well in the 'very easy' to 'medium' Sudoku puzzles, but then significantly underperformed in the 'hard' puzzles (relative to the others). Looking more closely at the tests themselves, it was clear to see that the earlier tests were significantly "simpler", in the sense that many of the cells had already been filled, than their harder counterparts. Remembering that complexity exponentially increases as the state space increases, this observation intuitively makes sense. Due to the algorithm simplicity, it also makes sense that solutions were found faster than for other approaches.

By introducing additional constraints, for example, the [Rules of Sudoku](https://www.sudokuonline.io/tips/sudoku-rules), and therefore limiting the search space, satisfactory solutions can be found faster ([_2fastbacktracking.py](_2fastbacktracking.py) is an example of implementing these constraints in a code efficient manner).

### Conclusion
Backtracking alone would solve the Sudoku problem, but would do poorly on more complex puzzles. Implementing heuristics to reduce the search space should be explored next to improve performance.

## Constraint Satisfaction Propagation
---
### Algorithm Approach
As in the backtracking approach, the CSP design recursively tests potential solution candidates. Rather than choosing a random value from 1 to 9, the CSP approach queries a bank of variables which satisfy a set of constraints, thereby reducing the search space; this is more formally written as [[ref](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)]:

X = {X<sub>1</sub>, X<sub>2</sub>, ... X<sub>n</sub>}   --> Set of variables

D = {D<sub>1</sub>, D<sub>2</sub>, ... D<sub>n</sub>}   --> Set of their respective domains of values

C = {C<sub>1</sub>, C<sub>2</sub>, ... C<sub>n</sub>}   --> Set of constraints.

Additionally, rather than selecting a random next value to test, a pool of "most likely candidates" are selected from. Below, are some of the key features implemented in this algorithm.

### Dictionary Representation (Faster Look-Ups)
As the CSP algorithm would continually look-up cells in the Sudoku matrix, it was decided that a dictionary representation would be most performant. Though Numpy operations are conducted in C, a lower level and faster programming language than Python, online sources state that Python dictionary look-ups can be up to x6.6 faster than list equivalents [[ref](https://towardsdatascience.com/faster-lookups-in-python-1d7503e9cd38)]. Moreover, the Sudoku puzzle was then reconstructed into a 1-dimensional representation to reduce the number of lookups and sub-list/ sub-dict requirements; below shows the keys of each Sudoku cell:

| 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  |
|----|----|----|----|----|----|----|----|----|
| 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 |
| 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 |
| 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 |
| 54 | 55 | 56 | 57 | 58 | 59 | 60 | 61 | 62 |
| 63 | 64 | 65 | 66 | 67 | 68 | 69 | 70 | 71 |
| 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 80 |

Another major benefit of adopting this approach was that all rules/ constraints in the Sudoku environment could be implemented in a single for loop, in range 0 to 8, by simply using some mathematical relationships; the high level code for this is presented below:

```python
        # eliminate value from columns and rows and boxes all at once
        ...
        for i in range( 9 ):
            # eliminate values from cols
            col_index = index - colloc + i
            if value in self.possible_values[ col_index ] and len(self.possible_values[ col_index ]) >= 1:
                self.possible_values[ col_index ].remove(value)

            # eliminate values from rows
            row_index = index - (self.row * rowloc) + (self.row * i)
            if value in self.possible_values[ row_index ] and len(self.possible_values[ row_index ]) >= 1:
                self.possible_values[ row_index ].remove(value)
        
            ...

            # eliminate values from boxes
            box_index = index + col_shift + row_shift
            if value in self.possible_values[ box_index ] and len(self.possible_values[ box_index ]) >= 1:
                self.possible_values[ box_index ].remove(value)
```

### Singleton Method
After adding the chosen value into the Sudoku solution, due to the constraints, some cells would only have x1 possible value remaining. In these cases, these values _must_ be filled into the solution. The singleton method would do exactly this and, as a result, reduce the number of branching nodes therefore reducing computation time; a diagramatic representation of this is presented below (note that the impact of deepcopy will be discussed in following sections):

<!-- ![Singleton Representation](/images/singleton.png "Singleton Benefits.") -->
<img src="/images/singleton.png" width="450">

Code representation of this method presented below:
```python
    def __set_singleton_cells( self ):
        """Writes values to cells which have exactly 1 possible value."""
        items = [-1]
        while any( items ): # after adding new singletons, sometimes more appear, while loop to catch them!
            items = [ (key,value) for key, value in self.possible_values.items() if len( value ) == 1 ]
            for key, value in items:
                if self.final_values[ key ] == 0 and len( value ) == 1: 
                    self.final_values[ key ] = value[0]
                    self.__eliminate_rcb( index = key )
```

### Most Constraining Cell
Adopting the approach of 'Most Constraining Cell' increases the probability that the algorithm will fail faster, therefore, closing off branches in the state space. Additionally, it will ensure that paths which have a limited number of available cells are tested first. Often, certain cells in Sudoku puzzles have a limited number of options, so it is favorable to place/enforce these values first. 
```python
def pick_next_cell( state ):
    """Return the index of the most constrained cell next."""
    vals = [ value for index, value in state.possible_values.items() if len(value) > 0 ]
    min_index = list( state.possible_values.values() ).index( min(vals, key=len) )
    return min_index
```

### Most Constraining Value
Similar to above, order the values in a sequence which is the most constraining. This approach counts the number of X's already placed in the Sudoku puzzle, and then prioritizes them in queue, with priority given to numbers which occur most frequently in the solution puzzle.
```python
def order_possible_values( state, index ):
    """Order the values so most constraining value (value placed most frequently) is chosen."""
    possVals = state.possible_values[ index ]
    values = [ num[0] for num in reversed(state.get_counts().most_common()) if num[0] in possVals ]
    return values
```

### Deepcopy and cPickle
Using the [Scalene](https://github.com/plasma-umass/scalene) Python performance profiler showed the Deepcopy function, used to copy each state before updating said state, to have a significant effect on algorithm performance, around 80% of total time taken (see image below).

![Deepcopy Impact](/images/deepcopy.png "Deepcopy showing significant performance limiter")

By replacing Deepcopy with the cPickle equivalent (a C compiled version of Deepcopy), total time taken to complete the coursework tests reduced by ~30%, as outlined in the table presented above. _Note that initially, a custom deepcopy function was tested but yielded no improvement and was therefore abandoned – the code remains and is commented out however._

**_Note that cPickle is part of Python3 standard library so is acceptable for use in this coursework._**

### Benefits of Cython
[Cython](https://www.infoworld.com/article/3250299/what-is-cython-python-at-the-speed-of-c.html) is a package which directly compiles Python code into C. By compiling the CSP code into C, a further performance gain of ~20% was seen; this makes sense as a significant proportion of the code consisted of Pythonic list and dictionary comprehensions. Unfortunately, implementing this package in the context of this coursework would require the code to be compiled onto the testing machine. While this is possible, it was deemed "too risky" to incorporate.

### Discussion
While the CSP approach was slower than backtracking on the 'very easy' to 'medium' puzzles, it performed significantly better on the 'hard' ones While the increased algorithm complexity likely caused this reduction in speed for the easier puzzles, the CSP design was more performant overall. Comparing this approach with other peers, it is clear that the dictionary representation, with the succinct approach to deleting available variables, noticeably improved overall performance. 

It was clear that copying states, despite using cPickle over Deepcopy was hindering performance however. In order to improve system performance and reduce memory usage, a mutable version of this code could be implemented (which would entail restoring eliminated variables).

### Conclusion
The CSP algorithm described here would be sufficient to solve any Sudoku problem without requiring a user to wait for any significant amount of time. Further improvements could be implemented by converting the approach from using immutable states/ objects to mutable ones. Rather than implementing this however, the Exact Cover approach was explored instead.


## Exact Cover with Algorithm X (No Dancing Links)
---
### Algorithm Approach
As [Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) puts it, Algorithm X 'is a _straightforward_ recursive, nondeterministic, depth-first, backtracking algorithm used by Donald Knuth to demonstrate an efficient implementation called DLX, which uses the dancing links technique.' The aim of this algorithm is to find the collection of subsets S<sup>*</sup> which have exactly **one** instance of those in collection S. For Sudoku puzzles with unique solutions, the exact cover approach is acceptable. Rather than presenting an example here, readers are directed to [here](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) for some demonstrative examples of this problem.

One disadvantage of this algorithm, discussed in [D. Knuth's paper on Dancing Links](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf), is the computational load created by repeatedly eliminating and restoring rows and columns in the matrix representation the problem space; to combat this, the Dancing Links approach is used. For this implementation, this approach was omitted due to design complexity however and, rather, the mutable approach described in the previous section was implemented – credit to A. Assaf who describes this approach [here](https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html).

### No Puzzle Pre-checker
For all other algorithms, a **check_sudoku( )** function was used to scan each puzzle before attempting a solution in order to avoid attempting to solve impossible problems. Due to the architecture of this algorithm, as well as its speed, this step was not necessary, thereby reducing overall algorithm complexity.

### Eliminate and Restoring RCVs (Rows, Cols and Boxes)
While a similar _eliminate_ function was used in the CSP approach, here, a _restore_ algorithm was also introduced in order to mitigate the requirements of a cPickle/ Deepcopying of each state. These two method implementations are presented below:

```python
    def __eliminateRCV( self, RCV : tuple ):
            """Delete all conflicting rcv's, but store them in a returned list.'"""
            rcvStore = list()
            for c in self.R[ RCV ]:   # for all the cols at current row
                for _rcv in self.C[ c ]: # for all the rcvs at current col (col and row now)
                    for _c in self.R[ _rcv ]: # for the col entries at current row
                        if _c != c: self.C[ _c ].remove( _rcv )
                rcvStore.append( self.C.pop( c ) )
            return rcvStore
```

```python
    def __restoreRCV( self, RCV, rcvStore : list ):
        """Restore the deleted rcv's that were passed as a list (opposite of eliminate method)."""
        for c in self.R[ RCV ][::-1]:
            self.C[ c ] = rcvStore.pop()
            for _rcv in self.C[ c ]:
                for _c in self.R[ _rcv ]:
                    if _c != c: self.C[ _c ].add( _rcv )
```

### Modified Backtracking (Restoring Mutable Data)
The only major change here is the inclusion of the 'unassign_value' after checking if a given state is a goal state i.e. if not a goal state then restore the value back to what it was before (and update S<sup>*</sup>).
```python
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
```

### Discussion
As outlined in the table at the start of this ReadMe, the overall performance improvements are significant using Algorithm X. What is interesting to see however is how the algorithm performed significantly worse when using the Deepcopy approach, where each new state is an immutable copy of the previous. 

In actuality, this does make intuitive sense however as each and every subset selection in the Algorithm X would generate a new Deepcopy state. In the CSP algorithm however, the singleton implementation ensured that many states would be _automatically_ enforced **before** moving to the next state. 

Fortunately, the mutable implementation of Algorithm X was sufficiently performant to negate the negative effects of not having a singleton method. To make this comparison more "fair", it would be interesting to modify the CSP algorithm to a mutable version in order to see whether the performance would improve by the same/ similar margin as in Algorithm X's case.

As a final observation, it is interesting to see that Algorithm X compute time appeared to scale linearly with puzzle complexity, whereas the other algorithms would take _seemingly_ exponentially longer with increasing puzzle difficulty; though this might be due to the increasing number of Deepcopy states being generated (hence the interest in a mutable CSP variation).

### Conclusion
Overall, the exact cover Algorithm X implementation was the fastest and, therefore was selected for the coursework submission.

## Future Improvements
---
1) **Dancing Links/ Algorithm DLX:** As described in D. Knuth's work, this approach reduces computational load and, therefore, is likely to further improve algorithm performance.
2) **Mutable CSP variation:** As mentioned above, a mutable version of the CSP algorithm might yield significant performance improvements above its current state.

# Useful Links/ Sources
---
1) [Optimisation of Algorithm](https://hexadix.com/hard-sudoku-solver-algorithm-part-2/)
2) [Analysis of Results (plots etc)](https://norvig.com/sudoku.html)
3) [EXACT COVER EXPLAINED](http://www.ams.org/publicoutreach/feature-column/fcarc-kanoodle#:~:text=Sudoku%20is%20also%20an%20exact%20cover%20problem&text=Every%20cell%20contains%20exactly%20one,one%20occurrence%20of%20each%20symbol.)
4) [Dancing Links](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)
5) [Algorithm X in 30 Lines](https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html)
6) [Exact Cover](https://en.wikipedia.org/wiki/Exact_cover#Detailed_example)
7) [Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)
8) [Doubly Linked List](https://en.wikipedia.org/wiki/Doubly_linked_list)
9) [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links)