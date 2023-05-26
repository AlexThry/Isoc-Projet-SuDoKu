import random
from pysat.formula import CNF

# Étape 1


def sudoku_to_sat(sudoku):
    cnf = CNF()

    # Ajouter des clauses pour chaque cellule
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                cnf.append([81*i + 9*j + sudoku[i][j]])
            else:
                for k in range(1, 10):
                    cnf.append([81*i + 9*j + k])

    # Ajouter des clauses pour chaque ligne, chaque colonne et chaque carré 3x3
    for i in range(9):
        for k in range(1, 10):
            cnf.append([81*i + 9*j + k for j in range(9)])
            cnf.append([81*j + 9*i + k for j in range(9)])
            cnf.append([81*(3*(i//3) + j//3) + 9 *
                       (3*(i % 3) + j % 3) + k for j in range(9)])

    # Ajouter des clauses pour s'assurer que chaque cellule ne représente pas deux chiffres différents en même temps
    for i in range(9):
        for j in range(9):
            for d in range(1, 10):
                for d_prime in range(d+1, 10):
                    cnf.append(
                        [-1*(81*i + 9*j + d), -1*(81*i + 9*j + d_prime)])

    return cnf

# Étape 2


def is_sudoku_solved(sudoku):
    for row in sudoku:
        if sorted(row) != list(range(1, 10)):
            return False

    for j in range(9):
        column = [sudoku[i][j] for i in range(9)]
        if sorted(column) != list(range(1, 10)):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [sudoku[i+k//3][j+k % 3] for k in range(9)]
            if sorted(square) != list(range(1, 10)):
                return False

    return True
# Étape 3


def is_valid(sudoku, row, col, num):
    # Vérifier la ligne
    for x in range(9):
        if sudoku[row][x] == num:
            return False

    # Vérifier la colonne
    for x in range(9):
        if sudoku[x][col] == num:
            return False

    # Vérifier le carré
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if sudoku[i + start_row][j + start_col] == num:
                return False

    return True


def solve_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(sudoku, i, j, num):
                        sudoku[i][j] = num
                        if solve_sudoku(sudoku):
                            return True
                        sudoku[i][j] = 0
                return False
    return True


if __name__ == '__main__':
    valid = False

    # Générer un SUDOKU semi-rempli
    semi_filled_sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    while valid == False:
        valid = solve_sudoku(semi_filled_sudoku)
        if valid == True:
            print(semi_filled_sudoku)
            print(is_sudoku_solved(semi_filled_sudoku))
