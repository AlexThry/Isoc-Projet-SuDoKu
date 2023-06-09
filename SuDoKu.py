import random
from pysat.formula import CNF
from time import *
from pybloom_live import BloomFilter
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


# def is_valid(sudoku, row, col, num):
#     # Vérifier la ligne
#     for x in range(9):
#         if sudoku[row][x] == num:
#             return False

#     # Vérifier la colonne
#     for x in range(9):
#         if sudoku[x][col] == num:
#             return False

#     # Vérifier le carré
#     start_row = row - row % 3
#     start_col = col - col % 3
#     for i in range(3):
#         for j in range(3):
#             if sudoku[i + start_row][j + start_col] == num:
#                 return False

#     return True


# def solve_sudoku(sudoku):
#     for i in range(9):
#         for j in range(9):
#             if sudoku[i][j] == 0:
#                 for num in range(1, 10):
#                     if is_valid(sudoku, i, j, num):
#                         sudoku[i][j] = num
#                         if solve_sudoku(sudoku):
#                             return True
#                         sudoku[i][j] = 0
#                 return False
#     return True

# Initialisez le filtre de Bloom
bloom_filter = BloomFilter(capacity=1000, error_rate=0.1)


def fill_zeros(sudoku):
    # Create a copy of the original list
    filled_sudoku = [row[:] for row in sudoku]
    for i in range(9):
        for j in range(9):
            if filled_sudoku[i][j] == 0:
                filled_sudoku[i][j] = random.randint(1, 9)
    return filled_sudoku


if __name__ == '__main__':

    semi_filled_sudoku = [[0, 0, 4, 6, 7, 8, 9, 1, 2],
                          [6, 7, 2, 1, 9, 5, 3, 4, 8],
                          [1, 9, 8, 3, 4, 2, 5, 6, 7],
                          [8, 5, 9, 7, 6, 1, 4, 2, 3],
                          [4, 2, 6, 8, 5, 3, 7, 9, 1],
                          [7, 1, 3, 9, 2, 4, 8, 5, 6],
                          [9, 6, 1, 5, 3, 7, 2, 8, 4],
                          [2, 8, 7, 4, 1, 9, 6, 3, 5],
                          [3, 4, 5, 2, 8, 6, 1, 0, 0]]

    valid = is_sudoku_solved(semi_filled_sudoku)
    i = 0
    while valid == False:
        sudoku = fill_zeros(semi_filled_sudoku)
        # Convertir le sudoku en tuple pour le stocker dans le filtre de Bloom
        sudoku_tuple = tuple(tuple(row) for row in sudoku)
        if bloom_filter.capacity == bloom_filter.__len__():
            print("capacité maximale atteinte")
            valid = True
        elif sudoku_tuple in bloom_filter:
            print("Cette tentative a déjà été faite.")
        else:
            bloom_filter.add(sudoku_tuple)
            print(sudoku)
            i += 1
            valid = is_sudoku_solved(sudoku)
    print(i)

    # code qui résout le sudoku
    # while valid == False:
    #     valid = solve_sudoku(semi_filled_sudoku)
    #     if valid == True:
    #         print(semi_filled_sudoku)
    #         print(is_sudoku_solved(semi_filled_sudoku))
