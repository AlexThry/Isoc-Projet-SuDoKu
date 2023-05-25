from pysat.formula import CNF
import random
from pysat.solvers import Glucose3


def encode_sudoku(grid):
    cnf = CNF()

    # Add cell, row, column and box constraints
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:  # If the cell is pre-filled
                cnf.append([81*i + 9*j + grid[i][j]])  # Append the clause
            else:  # If the cell is not pre-filled
                # Add clauses for the cell, row, column and box constraints
                for val in range(1, 10):
                    cnf.append(
                        [-((81*(i//3) + 9*(j//3) + (3*(i % 3) + (j % 3)))*9 + val), 81*i + 9*j + val])

    return cnf


def is_sudoku_solved(vector):
    grid = [vector[i*9:(i+1)*9] for i in range(9)]

    # Check rows
    for row in grid:
        if len(set(row)) != 9 or 0 in row:
            return False

    # Check columns
    for col in zip(*grid):
        if len(set(col)) != 9:
            return False

    # Check boxes
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = [grid[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            if len(set(box)) != 9:
                return False

    return True


def try_random_solutions(cnf):
    solver = Glucose3()

    # Add the clauses to the solver
    for clause in cnf.clauses:
        solver.add_clause(clause)

    # Try random solutions
    for _ in range(100):  # Try 100 random solutions
        random_solution = [random.choice([True, False]) for _ in range(81*9)]
        if solver.solve(assumptions=random_solution):
            solution = solver.get_model()
            sudoku_solution = [i for i in solution if i > 0]
            if is_sudoku_solved(sudoku_solution):
                print("Sudoku solved!")
                return sudoku_solution

    print("No solution found.")
    return None


if __name__ == "__main__":
    # Test your code with a Sudoku grid
    grid = [
        [0, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 0, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 0, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    print
    done = False
    while done == False:
        cnf = encode_sudoku(grid)
        solution = try_random_solutions(cnf)
        if solution:
            print("Solution found:")
            done = True
            print(solution)
        else:
            print("No solution found.")
