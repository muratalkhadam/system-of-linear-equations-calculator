import numpy as np


class Matrix:
    def __init__(self, rows=0, columns=0, matr=[]):
        self.__rows = rows
        self.__columns = columns
        self.__matr = np.array(matr)

    def __mul__(self, num):
        a = Matrix(self.__rows, self.__columns, self.__matr)
        for i in range(a.__rows):
            for j in range(a.__columns):
                a.__matr[i][j] = a.__matr[i][j] * num
        return a

    def set_matr(self, value, i, j):
        self.__matr[i][j] = value

    def get_matr(self):
        return self.__matr

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns

    def get_determinate(self):
        return np.linalg.det(self.__matr)

    def delete_row(self, index):
        self.__matr = np.delete(self.__matr, index, 0)
        self.__rows -= 1

    def delete_column(self, index):
        self.__matr = np.delete(self.__matr, index, 1)
        self.__columns -= 1

    def copy_matr(self):
        temp = []
        for i in range(self.__rows):
            row = []
            for j in range(self.__columns):
                row.append(self.__matr[i][j])
            temp.append(row)
        return Matrix(self.__rows, self.__columns, temp)

    # алгебраичекое дополнение
    def get_alg_complements(self, i, j):
        temp = Matrix(self.__rows, self.__columns, self.__matr)
        temp.delete_row(i)
        temp.delete_column(j)
        return (-1)**(i+j+2) * temp.get_determinate()

    def transpose(self):
        temp = self.copy_matr()
        for i in range(self.__rows):
            for j in range(self.__columns):
                self.__matr[i][j] = temp.__matr[j][i]

    # присоединённая матрица
    def get_adjugate_matr(self):
        matr = []
        for i in range(self.__rows):
            row = []
            for j in range(self.__columns):
                a = self.get_alg_complements(i, j)
                row.append(a)
            matr.append(row)
        return Matrix(self.__rows, self.__columns, matr)

    def is_singular(self):
        if self.get_determinate() == 0:
            return True
        else:
            return False

    def get_invertible_matr(self, additional, det):
        result = additional * (1 / det)     # 1 / det(A) * (C*)transpose | matrix * const
        return result

    def mult(self, a):
        C = []
        for i in range(self.__rows):
            for j in range(a.__columns):
                total = 0
                for k in range(self.__columns):
                    total += self.__matr[i][k] * a.__matr[k][j]
                C.append(total)
        return C

    def is_simetrical(self):
        for i in range(1, len(self.__matr)):
            for j in range(i):
                if self.__matr[i][j] != self.__matr[j][i]:
                    return False
        return True

    def solve_triangle(self, b, lower=True):
        res = [[0] for _ in range(self.__rows)]
        col = self.__columns

        if lower:
            res[0][0] = b[0][0] / self.__matr[0][0]
            for i in range(1, col):
                temp = b[i][0]
                for j in range(1, i + 1):
                    temp -= self.__matr[i][j - 1] * res[j - 1][0]
                res[i][0] = temp / self.__matr[i][i]
        else:
            res[col - 1][0] = b[col - 1][0] / self.__matr[col - 1][col - 1]
            for i in range(col - 2, -1, -1):
                temp = b[i][0]
                for j in range(i + 1, col):
                    temp -= self.__matr[i][j] * res[j][0]
                res[i][0] = temp / self.__matr[i][i]

        return res

    def pivot_matrix(self):
        """Returns the pivoting matrix for M, used in Doolittle's method."""
        m = self.__rows
        # Create an identity matrix, with floating point values
        id_mat = [[float(i == j) for i in range(m)] for j in range(m)]
        # Rearrange the identity matrix such that the largest element of
        # each column of M is placed on the diagonal of of M
        for j in range(m):
            row = max(range(j, m), key=lambda i: abs(self.__matr[i][j]))
            if j != row:
                # Swap the rows
                id_mat[j], id_mat[row] = id_mat[row], id_mat[j]

        return Matrix(m, m, id_mat)
