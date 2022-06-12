from constants import COLOR, TEXT_HEIGHT, TEXT_WIDTH, GRAPHIC_HEIGHT, GRAPHIC_WIDTH
from classes.Plot import *
from classes.Matrix import *

import math
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class SolutionWindow:
    def __init__(self, parent, picked_method, A, B, height=600, width=600, title="Solution window",
                 resizable=(False, False)):
        self.__root = tk.Toplevel(parent)
        self.__root.geometry(f"{height}x{width}")
        self.__root.title(title)
        self.__root.resizable(resizable[0], resizable[1])
        self.__root["bg"] = COLOR

        self.__method = picked_method
        self.__text = tk.Text(self.__root, height=30, width=72)

        self.__matr_a: Matrix = A
        self.__matr_b: Matrix = B

        self.__iterations = 0

    # повертає корінь вікна
    def get_root(self):
        return self.__root

    # візуалізація коренів для системи з двома невідомими
    def visualize_roots(self, roots):
        self.__root.geometry(f"{GRAPHIC_HEIGHT}x{GRAPHIC_WIDTH}")
        self.__root.resizable(False, False)
        self.__text["height"] = TEXT_HEIGHT
        self.__text["width"] = TEXT_WIDTH

        plot = Plot(self.__matr_a, self.__matr_b, roots)

        canvas = FigureCanvasTkAgg(plot.get_fig(), master=self.__root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=50)

        tool_frame = tk.Frame(self.__root, bg=COLOR)
        tool_frame.grid(row=0, column=1, sticky="n")
        NavigationToolbar2Tk(canvas, tool_frame)

    # LUP-метод
    def lup_method(self):
        n = self.__matr_a.get_rows()

        L = Matrix(n, n, [[0.0] * n for i in range(n)])
        U = Matrix(n, n, [[0.0] * n for i in range(n)])

        P = self.__matr_a.pivot_matrix()
        PA = Matrix(n, n, np.array(P.mult(self.__matr_a)).reshape(n, n))

        for j in range(n):
            L.set_matr(1.0, j, j)
            self.__iterations += 1

            for i in range(j + 1):
                s1 = 0
                for k in range(i):
                    s1 += U.get_matr()[k][j] * L.get_matr()[i][k]
                    self.__iterations += 1

                U.set_matr(PA.get_matr()[i][j] - s1, i, j)
                self.__iterations += 1

            for i in range(j, n):
                s2 = 0
                for k in range(j):
                    s2 += U.get_matr()[k][j] * L.get_matr()[i][k]
                    self.__iterations += 1

                L.set_matr((PA.get_matr()[i][j] - s2) / U.get_matr()[j][j], i, j)
                self.__iterations += 1

        Pb = Matrix(P.get_rows(), self.__matr_b.get_columns(), np.array(P.mult(self.__matr_b)).reshape(P.get_rows(),
                                                                self.__matr_b.get_columns()))
        y_matr = L.solve_triangle(Pb.get_matr(), lower=True)
        y = Matrix(len(y_matr), len(y_matr[0]), y_matr)

        x = U.solve_triangle(y.get_matr(), lower=False)
        return x

    # Матричний метод
    def matrix_method(self):
        a_determinant = self.__matr_a.get_determinate()

        additional_matrix, self.__iterations = self.__matr_a.get_additional_matr(self.__iterations)

        additional_matrix.transpose()

        inverted, self.__iterations = self.__matr_a.get_invertible_matr(
            additional_matrix, a_determinant, self.__iterations
        )

        x = inverted.mult(self.__matr_b)

        return np.array(x).reshape(len(x), 1)

    # Метод Гауса-Холецького (квадратного кореня)
    def choletsky_method(self):
        L = Matrix(self.__matr_a.get_rows(), self.__matr_a.get_columns(), np.zeros(self.__matr_a.get_matr().shape))

        try:
            L.set_matr(math.sqrt(self.__matr_a.get_matr()[0][0]), 0, 0)

            for i in range(1, self.__matr_a.get_rows()):
                L.set_matr(self.__matr_a.get_matr()[i][0] / L.get_matr()[0][0], i, 0)
                self.__iterations += 1

            for i in range(1, self.__matr_a.get_rows()):
                for j in range(1, self.__matr_a.get_columns()):
                    if i == j:
                        temp = 0
                        for k in range(i):
                            temp += L.get_matr()[i][k] ** 2
                            self.__iterations += 1

                        L.set_matr(math.sqrt(self.__matr_a.get_matr()[i][i] - temp), i, i)
                        self.__iterations += 1
                    if j > i:
                        temp = 0
                        for k in range(i):
                            temp += L.get_matr()[i][k] * L.get_matr()[j][k]
                            self.__iterations += 1

                        L.set_matr((self.__matr_a.get_matr()[j][i] - temp) / L.get_matr()[i][i], j, i)
                        self.__iterations += 1

            L_trans = L.copy_matr()
            L_trans.transpose()

            y = L.solve_triangle(self.__matr_b.get_matr(), lower=True)
            x = L_trans.solve_triangle(y, lower=False)
            return x
        except:
            return None

    # реалізація зберігання рішення у файл
    def save_as_file(self):
        try:
            save_as = fd.asksaveasfilename(defaultextension=".txt")
            with open(save_as, "w") as file:
                file.write(self.__text.get("1.0", tk.END))
                mb.showinfo("Warning", "Файл був успішно збережений!")
        except FileNotFoundError:
            mb.showerror("Error", "Ви не зберегли результати у файл!")
        finally:
            mb.showinfo("Warning", "Робота з файлами завершена!")

    # заповнення форми відповідним рішенням
    def display(self):
        if self.__method == "LUP-метод":
            roots = self.lup_method()

        elif self.__method == "Матричний метод":
            roots = self.matrix_method()

        elif self.__method == "Метод Гауса-Холецького":
            roots = self.choletsky_method()

        if roots is not None:
            temp = ""
            temp += "Matrix A:\n"
            for i in range(self.__matr_a.get_rows()):
                for j in range(self.__matr_a.get_columns()):
                    temp_matr = str(self.__matr_a.get_matr()[i][j])
                    temp += temp_matr + " "*(8 - len(temp_matr))
                temp += "\n"
            temp += "Matrix B:\n"
            for i in range(self.__matr_b.get_rows()):
                temp += str(self.__matr_b.get_matr()[i][0]) + "\n"
            for i in range(len(roots)):
                root_to_display = round(roots[i][0], 3)
                temp += f"\nX{i+1} = {root_to_display}"
            temp += f"\nAmount of operations is {self.__iterations}"

            self.__text.insert(1.0, temp)
            save_button = tk.Button(self.__root, text="Save as file", command=self.save_as_file, width=10)
            save_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            if self.__matr_a.get_rows() == 2:
                self.visualize_roots(roots)
        else:
            self.__text.insert(1.0, "На етапі розв'язання було неможливо знайти корінь з від'ємного числа.\n"
                                  "Для данної матриці неможливо застосувати метод Гауса-Холецьокого,\n"
                                    "незважаючи що матриця є додатньовизначена та симетрична.")

        self.__text.config(state="disabled")
        self.__text.grid(row=0, column=0, padx=10, pady=10, sticky="w")
