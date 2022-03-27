# Code Description
The contents enclosed in this repository explore how the backtracking (BT), constraint satisfaction propagation (CSP) and exact cover (EC) algorithm performances differ in the context of solving Sudoku puzzles of varying complexity. For each of these alogrithms, various modifications were made to reduce computational time and memory usage; the results of said experiments have been presented below. 

Overall, the Exact Cover, Algorithm X (without Dancing Links) approach outperformed all other algorithms (on average) and, as such, was selected for submission.


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
| Script Name           | **Algorithm**                                           | **Very Easy [ms]** | **Easy [ms]** | **Medium [ms]** | **Hard [ms]** | **Total [ms]** |
|-----------------------|---------------------------------------------------------|--------------------|---------------|-----------------|---------------|----------------|
| _1backtracking.py     | Backtracking                                            |         21         |       20      |        47       |     365278    |     365475     |
| _2fastbacktracking.py | [Fast Backtracking](https://github.com/techtribeyt/sudoku/blob/main/code.py)     |         13         |       14      |        13       |      6822     |      6768      |
| _3CSP.py              | Constraint Satisfaction Propagation – Deepcopy          |         37         |       34      |        56       |      3254     |      3411      |
| _3CSP.py              | Constraint Satisfaction Propagation – cPickle           |         36         |       34      |        56       |      2341     |      2442      |
| _4Exact_Cover_DC.py   | Exact Cover, Algorithm X (no Dancing Links) – Deepcopy  |         851        |      599      |       2241      |     13324     |      17200     |
| _4Exact_Cover_WO.py   | Exact Cover, Algorithm X (no Dancing Links) – W.O. Copy |         52         |       53      |        55       |       92      |       246      |

### World's Hardest Sudoku Puzzle
---
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

| Script Name           | **Algorithm**                                                                 | **Very Hard [ms]** |
|-----------------------|-------------------------------------------------------------------------------|--------------------|
| _1backtracking.py     | Backtracking                                                                  |        1915        |
| _2fastbacktracking.py | [Fast Backtracking](https://github.com/techtribeyt/sudoku/blob/main/code.py)  |         135        |
| _3CSP.py              | Constraint Satisfaction Propagation – Deepcopy                                |          23        |
| _3CSP.py              | Constraint Satisfaction Propagation – cPickle                                 |          15        |
| _4Exact_Cover_DC.py   | Exact Cover, Algorithm X (no Dancing Links) – Deepcopy                        |       26369        |
| _4Exact_Cover_WO.py   | Exact Cover, Algorithm X (no Dancing Links) – W.O. Copy                       |          75        |



### Sudoku Generator
SUDOKU GENERATOR INSIDE THE TESTS.PY SCRIPT FILE --> THIS WAS USEFUL FOR FINDING OUT VARIOUS ALGORITHM WEAKNESSES
mention very hard suduko puzzle benchmark


## Backtracking
### Algorithm Approach
### Backtracking Algorithm
### Fast Backtracking


## Constraint Satisfaction Propagation
### Algorithm Approach
### Key Features

## Deepcopy and cPickle
![Deepcopy Impact](/images/deepcopy.png "Deepcopy showing significant performance limiter")

## Exact Cover with Algorithm X (No Dancing Links)
### Algorithm Approach
### Key Features

## Benefits of Cythonize


## Future Improvements
DANCING LINKS!!




HIGH LEVEL SUMMARY OF THE WORK AND THEN TOUCH ON THE RESULTS FROM TESTING. MENTION DATA STRUCTURE! Don't need a pre-cheker with contstraint satisfaction because the constraints are such that a solution will never be found anyway


# Useful Links/ Sources
1) Iterative Hill Climbing... what are the impacts of this? Remember to do tie breaking, else will continually test same branches
2) Mutability of objects, better to not deepcopy and just overwrite the object? Is this true? Discuss
3) [Optimisation of Algorithm](https://hexadix.com/hard-sudoku-solver-algorithm-part-2/)
4) [Analysis of Results (plots etc)](https://norvig.com/sudoku.html)
5) [EXACT COVER EXPLAINED](http://www.ams.org/publicoutreach/feature-column/fcarc-kanoodle#:~:text=Sudoku%20is%20also%20an%20exact%20cover%20problem&text=Every%20cell%20contains%20exactly%20one,one%20occurrence%20of%20each%20symbol.)
6) [Dancing Links](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)
7) [Algorithm X in 30 Lines](https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html)
8) [Exact Cover](https://en.wikipedia.org/wiki/Exact_cover#Detailed_example)
9) [Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)
10) [Doubly Linked List](https://en.wikipedia.org/wiki/Doubly_linked_list)
11) [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links)