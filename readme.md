# Code Description
HIGH LEVEL SUMMARY OF THE WORK AND THEN TOUCH ON THE RESULTS FROM TESTING


## Testing Methods
### Core Tests
| Script Name           | **Algorithm**                                           | **Very Easy [ms]** | **Easy [ms]** | **Medium [ms]** | **Hard [ms]** | **Total [ms]** |
|-----------------------|---------------------------------------------------------|--------------------|---------------|-----------------|---------------|----------------|
| 1_backtracking.py     | Backtracking                                            |         21         |       20      |        47       |       –       |        –       |
| 2_fastbacktracking.py | [Fast Backtracking](https://github.com/techtribeyt/sudoku/blob/main/code.py)     |         13         |       14      |        13       |      6822     |      6768      |
| 3_CSP.py              | Constraint Satisfaction Propagation – Deepcopy          |         37         |       34      |        56       |      3254     |      3411      |
| 3_CSP.py              | Constraint Satisfaction Propagation – cPickle           |         36         |       34      |        56       |      2341     |      2442      |
| 4_Exact_Cover_DC.py   | Exact Cover, Algorithm X (no Dancing Links) – Deepcopy  |         851        |      599      |       2241      |     13324     |      17200     |
| 4_Exact_Cover_WO.py   | Exact Cover, Algorithm X (no Dancing Links) – W.O. Copy |         52         |       53      |        55       |       92      |       246      |
### Sudoku Generator


## Backtracking
### Algorithm Approach
### Backtracking Algorithm
### Fast Backtracking


## Constraint Satisfaction Propagation
### Algorithm Approach
### Key Features
### Deepcopy and cPickle
![Deepcopy Impact](/images/deepcopy.png "Deepcopy showing significant performance limiter")


## Exact Cover with Algorithm X (No Dancing Links)
### Algorithm Approach
### Key Features


## Benefits of Cythonize


## Future Improvements
DANCING LINKS!!


# Thoughts
1) Iterative Hill Climbing... what are the impacts of this? Remember to do tie breaking, else will continually test same branches
2) Mutability of objects, better to not deepcopy and just overwrite the object? Is this true? Discuss
3) [Optimisation of Algorithm](https://hexadix.com/hard-sudoku-solver-algorithm-part-2/)
4) [Analysis of Results (plots etc)](https://norvig.com/sudoku.html)