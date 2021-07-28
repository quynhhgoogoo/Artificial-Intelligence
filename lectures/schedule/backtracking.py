VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]
CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]


def backtrack(assignment):
    '''Run backtracking search to find an assignment'''

    # Check if assignment is compeleted
    if len(assignment) == len(VARIABLES):
        return assignment

    # Assign a new variable
    var = select_unassigned_variable(assignment)
    for value in ["Monday", "Tuesday", "Wednesday"]:
        
        # Add newly assigned variable as a value inside dictionary 
        new_assignment = assignment.copy()
        new_assignment[var] = value

        # If assignment value is consistent, continue assigning value to next node
        if consistent(new_assignment):
            # Adding new variable recursively to assignment until unassigned list is empty
            result = backtrack(new_assignment)
            if result is not None:
                return result
    
    return None


def select_unassigned_variable(assignment):
    '''Choose variable which is not yet assigned, in order'''
    for variable in VARIABLES:
        if variable not in assignment:
            return variable
    return None


def consistent(assignment):
    '''Check if an assignment is consistent'''
    for (x,y) in CONSTRAINTS:

        # Consider arc where both are assigned
        if x not in assignment or y not in assignment:
            continue

        # If both nodes have same value, they are not consistent
        if assignment[x] == assignment[y]:
            return False
    return True


if __name__ == '__main__':
    solution = backtrack(dict())
    print("Solution: ", solution)