import tkinter as tk
import math
import tkinter.filedialog as fd
import tkinter.messagebox as mb
# from constants import COLOR
# import numpy as np
# import matplotlib.pyplot as plt
# from sympy import plot_implicit, Eq
# from scipy.linalg import solve_triangular
# from sympy.abc import x, y
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from classes.Plot import *
from classes.Matrix import *


class SolutionWindow:
    def __init__(self, parent, picked_method, A, B, height=585, width=600, title="Solution window",
                 resizable=(True, True)):
        self.__root = tk.Toplevel(parent)
        self.__root.geometry(f"{height}x{width}")
        self.__root.title(title)
        self.__root.resizable(resizable[0], resizable[1])
        self.__root["bg"] = "pink"

        self.__method = picked_method
        self.__text = tk.Text(self.__root, height=27, width=70)

        self.__a: Matrix = A
        self.__b: Matrix = B

    def get_root(self):
        return self.__root

    # work with matplotlib
    def visualize_roots(self, roots):
        self.__root.geometry("800x500")
        self.__root.resizable(False, False)
        self.__text["height"] = 10
        self.__text["width"] = 20
        # plot = Plot()
        # plot = Plot()
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        up = 50
        low = -50
        step = 0.5
        x = np.arange(low, up, step)
        plt.scatter(roots[0][0], roots[1][0], s=150)

        for i in range(2):
            x = np.arange(low, up, step)
            if self.__a.get_matr()[i][1] != 0:
                y = (self.__b.get_matr()[i][0] - self.__a.get_matr()[i][0] * x) / self.__a.get_matr()[i][1]
            else:
                # fix vertical line
                # 14*x + 0*y = -5
                x = [self.__b.get_matr()[i][0] / self.__a.get_matr()[i][0] for _ in range(int((up - low) / step))]
                y = np.arange(low, up, step)
                # x = self.__b.get_matr()[i][0] / self.__a.get_matr()[i][0]

            text = f"{round(self.__a.get_matr()[i][0], 3)}*X1 "

            if self.__a.get_matr()[i][1] < 0:
                text += f"{round(self.__a.get_matr()[i][1], 3)}*X2 = "
            else:
                text += f"+ {round(self.__a.get_matr()[i][1], 3)}*X2 = "

            text += str(round(self.__b.get_matr()[i][0], 3))

            if i == 0:
                # ax.plot(x, y, color="r", label=text)
                ax.plot(x, y, color="r", label=text)
            else:
                ax.plot(x, y, color="g", label=text)

        # plt.scatter(roots[0], roots[1], s=150)
        plt.xlabel("X1")
        plt.ylabel("X2")
        ax.legend(loc="best")
        # print(x)
        # print(y)
        # fig.add_subplot(211).plot(x, y, color="r", label="tesgdfgdt1")
        # fig.add_subplot(212).plot(x, y, color="g", label="tedfgdfgdst2")

        canvas = FigureCanvasTkAgg(fig, master=self.__root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=50, sticky="e")

        # fig.add_subplot(211).plot(x, y)
        # canvas = FigureCanvasTkAgg(fig, master=self.__root)
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)
        # print("123")
        # canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)

    @staticmethod
    def lup_method(a: Matrix, b: Matrix):
        """Performs an LU Decomposition of A (which must be square)
        into PA = LU. The function returns P, L and U."""
        n = a.get_rows()
        # Create zero matrices for L and U
        L = Matrix(n, n, [[0.0] * n for i in range(n)]) # list[list]
        U = Matrix(n, n, [[0.0] * n for i in range(n)]) # list[list]
        # Create the pivot matrix P and the multipled matrix PA
        P = a.pivot_matrix()
        PA = Matrix(n, n, np.array(P.mult(a)).reshape(n, n))
        # print(PA.get_matr())
        # Perform the LU Decomposition
        for j in range(n):
            # All diagonal entries of L are set to unity
            L.set_matr(1.0, j, j)

            # LaTeX: u_{ij} = a_{ij} - \sum_{k=1}^{i-1} u_{kj} l_{ik}
            for i in range(j + 1):
                s1 = sum(U.get_matr()[k][j] * L.get_matr()[i][k]
                         for k in range(i))
                U.set_matr(PA.get_matr()[i][j] - s1, i, j)

            # LaTeX: l_{ij} = \frac{1}{u_{jj}} (a_{ij} - \sum_{k=1}^{j-1} u_{kj} l_{ik} )
            for i in range(j, n):
                s2 = sum(U.get_matr()[k][j] * L.get_matr()[i][k]
                         for k in range(j))
                L.set_matr((PA.get_matr()[i][j] - s2) / U.get_matr()[j][j], i, j)
        # PA = LU
        # Ax = B
        # PAX = PB

        # y = Ux
        # Ly = Pb -> forward
        # Ux = y -> backward
        # PA = Matrix(n, n, np.array(P.mult(a)).reshape(n, n))
        # Pb = P.mult(b)
        Pb = Matrix(P.get_rows(), b.get_columns(), np.array(P.mult(b)).reshape(P.get_rows(), b.get_columns()))

        y_matr = L.solve_triangle(Pb.get_matr(), lower=True)
        y = Matrix(len(y_matr), len(y_matr[0]), y_matr)

        x = U.solve_triangle(y.get_matr(), lower=False)

        return x

    @staticmethod
    def matrix_method(a: Matrix, b: Matrix):
        a_determinant = a.get_determinate()

        additional_matrix = a.get_adjugate_matr()

        additional_matrix.transpose()

        inverted = a.get_invertible_matr(additional_matrix, a_determinant)

        x = inverted.mult(b)
        return np.array(x).reshape(len(x), 1)

    @staticmethod
    def choletsky_method(a: Matrix, b: Matrix):
        L = Matrix(a.get_rows(), a.get_columns(), np.zeros(a.get_matr().shape))
        try:
            L.set_matr(math.sqrt(a.get_matr()[0][0]), 0, 0)
            # fill the first column
            for i in range(1, a.get_rows()):
                L.set_matr(a.get_matr()[i][0] / L.get_matr()[0][0], i, 0)

            for i in range(1, a.get_rows()):
                for j in range(1, a.get_columns()):
                    if i == j:
                        temp = 0
                        for k in range(i):
                            temp += L.get_matr()[i][k] ** 2
                        L.set_matr(math.sqrt(a.get_matr()[i][i] - temp), i, i)
                    if i < j:
                        temp = 0
                        for k in range(i):
                            temp += L.get_matr()[i][k] * L.get_matr()[j][k]
                        L.set_matr((a.get_matr()[j][i] - temp) / L.get_matr()[i][i], j, i)
            L_trans = L.copy_matr()
            L_trans.transpose()

            y = L.solve_triangle(b.get_matr(), lower=True)
            x = L_trans.solve_triangle(y, lower=False)
            return x
        except:
            return None

    def save_as_file(self):
        try:
            save_as = fd.asksaveasfilename(defaultextension=".txt")
            with open(save_as, "w") as file:
                file.write(self.__text.get("1.0", tk.END))
        except FileNotFoundError:
            mb.showerror("Error", "You didn't save file!")
        finally:
            mb.showinfo("Warning", "Work with files ends")

    def display(self):
        iterations = 0
        if self.__method == "lup":
            to_display = self.lup_method(self.__a, self.__b)

        if self.__method == "matrix":
            to_display = self.matrix_method(self.__a, self.__b)

        if self.__method == "gause":
            to_display = self.choletsky_method(self.__a, self.__b)

        if to_display is not None:
            temp = ""
            temp += "Matrix A:\n"
            for i in range(self.__a.get_rows()):
                for j in range(self.__a.get_columns()):
                    temp_matr = str(self.__a.get_matr()[i][j])
                    temp += temp_matr + " "*(8 - len(temp_matr))
                temp += "\n"
            temp += "Matrix B:\n"
            for i in range(self.__b.get_rows()):
                temp += str(self.__b.get_matr()[i][0]) + "\n"
            for i in range(len(to_display)):
                temp += f"\nX{i+1} = {round(to_display[i][0], 3)}"

            self.__text.insert(1.0, temp)
            save_button = tk.Button(self.__root, text="Save as file", command=self.save_as_file, width=10)
            save_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            if self.__a.get_rows() == 2:
                self.visualize_roots(to_display)
        else:
            # print(self.method)
            self.__text.insert(1.0, "На этапе решения было невозможно извлечь корень из отрицательного числа.\n"
                                  "Для данной матрицы нельзя применить данный метод")

        self.__text.config(state="disabled")
        self.__text.grid(row=0, column=0, padx=10, pady=10, sticky="w")
