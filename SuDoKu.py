class SuDoKu:
    def __init__(self, grid: list) -> None:
        """
        Sudoku
        :param grid: liste de 9 listes de 9 valeurs
        """
        self.grid = grid

    def __str__(self) -> str:
        """
        Affiche le Sudoku de façon matricielle
        :return: str
        """
        res = "["
        for i in range(9):
            res += "["
            for j in range(9):
                res += str(self.grid[i][j])
                if j != len(self.grid[i])-1:
                    res += ", "
            res += "]"
            if i != len(self.grid) - 1:
                res += "\n"
        res += "]"
        return res

    def checkColumn(self, colIndex: int) -> bool:
        """
        Vérifie qu'une colonne soit consistante
        :param colIndex: int, numéro de la colonne à vérifier
        :return: boolean
        """
        assert colIndex >= 0 and colIndex < 9, "colIndex must be between 0 and 8."
        check = []
        i = 0
        res = True
        while i < 9 and res == True:
            val = self.grid[i][colIndex]
            if val in check or val > 9 or val < 1:
                res = False
            check.append(val)
            i += 1
        return res



    def checkLine(self, linIndex: int) -> bool:
        """
        Vérifie qu'une ligne soit consistante
        :param linIndex: int, numéro de la ligne à vérifier
        :return: boolean
        """
        assert linIndex >= 0 and linIndex < 9, "linIndex must be between 0 and 8."
        check = []
        i = 0
        res = True
        while i < 9 and res == True:
            val = self.grid[linIndex][i]
            if val in check or val > 9 or val < 1:
                res = False
            check.append(val)
            i += 1
        return res


    def checkRegion(self, x: int, y: int) -> bool:
        """
        Vérifie qu'une région est consistante
        :param x: int, index de la region sur l'axe principal, comrpris entre 0 et 2 compris.
        :param y: int, index de la region sur l'axe secondaire, comrpris entre 0 et 2 compris.
        :return: boolean
        """
        assert x >= 0 and x < 3, "x must be between 0 and 2."
        assert y >= 0 and y < 3, "y must be between 0 and 2."

        check = []
        i = x*3
        j = y*3
        res = True

        while i < x*3+3 and res == True:
            while j < y*3+3 and res == True:
                val = self.grid[i][j]
                # print(val, check)
                if val in check or val < 1 or val > 9:
                    res = False
                j += 1
                check.append(val)
            i += 1
            j = y * 3
        return res


    def checkAllRegions(self) -> bool:
        """
        Vérifie que toutes les régions soient consistantes
        :return: boolean
        """
        res = True
        i = 0
        j = 0
        while i < 3 and res == True:
            while j < 3 and res == True:
                res = self.checkRegion(i, j)
                j += 1
            j = 0
            i += 1
        return res

    def checkAllColAndLin(self) -> bool:
        """
        Vérifie que toutes les lignes et toutes les colonnes soient consistantes
        :return: boolean
        """
        i = 0
        j = 0
        res = True
        while i < 9 and res == True:
            if not self.checkColumn(i):
                res = False
            if not self.checkLine(i):
                res = False
            i += 1
        return res


    def checkSudoku(self) -> bool:
        """
        Vérifie que le sudoku soit consistant
        :return: boolean
        """
        if self.checkAllRegions() and self.checkAllColAndLin():
            res = True
        else:
            res = False
        return res


