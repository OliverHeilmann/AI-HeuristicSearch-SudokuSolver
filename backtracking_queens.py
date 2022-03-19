import random
import copy, time

class PartialEightQueensState:
    def __init__(self, n=8):
        self.n = n

        # a list of possible values for each column
        self.possible_values = [[i for i in range(0, self.n)] for _ in range(0, self.n)]
        self.final_values = [-1] * self.n

    def is_goal(self):
        """This partial state is a goal state if every column has a final value"""
        return all(value != -1 for value in self.final_values)

    def is_invalid(self):
        """This partial state is invalid if any column has no possible values"""
        return any(len(values) == 0 for values in self.possible_values)

    def get_possible_values(self, column):
        return self.possible_values[column].copy()

    def get_final_state(self):
        if self.is_goal():
            return self.final_values
        else:
            return -1

    def get_singleton_columns(self):
        """Returns the columns which have no final value but exactly 1 possible value"""
        return [index for index, values in enumerate(self.possible_values)
                if len(values) == 1 and self.final_values[index] == -1]

    def set_value(self, column, row):
        """Returns a new state with this column set to this row, and the change propagated to other domains"""
        if row not in self.possible_values[column]:
            raise ValueError(f"{row} is not a valid choice for column {column}")

        # create a deep copy: the method returns a new state, does not modify the existing one
        state = copy.deepcopy(self)

        # update this column
        state.possible_values[column] = [row]
        state.final_values[column] = row

        # now update all other columns possible values
        # start with columns to the left
        for update_col in range(0, column):
            # remove same row
            if row in state.possible_values[update_col]:
                state.possible_values[update_col].remove(row)

            # remove upper diagonal
            upper_diag = row + (column - update_col)
            if upper_diag in state.possible_values[update_col]:
                state.possible_values[update_col].remove(upper_diag)

            # lower diagonal
            lower_diag = row - (column - update_col)
            if lower_diag in state.possible_values[update_col]:
                state.possible_values[update_col].remove(lower_diag)

        # now update columns to the right
        for update_col in range(column + 1, state.n):
            # remove same row
            if row in state.possible_values[update_col]:
                state.possible_values[update_col].remove(row)

            # remove upper diagonal
            upper_diag = row + (update_col - column)
            if upper_diag in state.possible_values[update_col]:
                state.possible_values[update_col].remove(upper_diag)

            # lower diagonal
            lower_diag = row - (update_col - column)
            if lower_diag in state.possible_values[update_col]:
                state.possible_values[update_col].remove(lower_diag)

        # if any other columns with no final value only have 1 possible value, make them final (just assigning the
        # values with only x1 option to the board i.e. they must go there for the strategy to work).
        singleton_columns = state.get_singleton_columns()
        while len(singleton_columns) > 0:
            col = singleton_columns[0]
            state = state.set_value(col, state.possible_values[col][0])
            singleton_columns = state.get_singleton_columns()

        return state


def pick_next_column(partial_state):
    """
    Used in depth first search, currently chooses a random 
    column that has more than one possible value
    """
    col_indices = [index for index, values in enumerate(partial_state.possible_values) if len(values) > 1]
    return random.choice(col_indices)   # col_indices.pop()


def order_values(partial_state, col_index):
    """
    Get values for a particular column in the 
    order we should try them in. Currently random.
    """
    values = partial_state.get_possible_values(col_index)
    random.shuffle(values)
    return values


def depth_first_search(partial_state=PartialEightQueensState()):
    """
    This will do a depth first search on partial states, trying 
    each possible value for a single column.

    Notice that we do not need to try every column: if we try 
    every possible value for a column and can't find a
    solution, then there is no possible value for this column, 
    so there is no solution.
    """
    depth_first_search.counter +=1

    col_index = pick_next_column(partial_state)
    values = order_values(partial_state, col_index)

    for value in values:
        new_state = partial_state.set_value(col_index, value)
        if new_state.is_goal():
            return new_state
        if not new_state.is_invalid():
            deep_state = depth_first_search(new_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state
    return None

depth_first_search.counter =0
partial_state = PartialEightQueensState(n=100)
start_time = time.process_time()
goal = depth_first_search(partial_state).get_final_state()
end_time = time.process_time()
total_time = end_time-start_time
# print(goal)
print(f"Nodes Explored: {depth_first_search.counter}\nTotal Time: {total_time}s")