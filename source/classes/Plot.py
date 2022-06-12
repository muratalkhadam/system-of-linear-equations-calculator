import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self, matr_a, matr_b, roots):
        self.__fig, self.__ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.__fill_plot(matr_a, matr_b, roots)

    # повертає створенне полотно
    def get_fig(self):
        return self.__fig

    # будує графіки з отримннах значень
    def __fill_plot(self, matr_a, matr_b, roots):
        up = 10
        low = -10
        step = 0.1

        x1 = roots[0][0]
        x2 = roots[1][0]

        for i in range(2):
            x = np.arange(x1 - 10, x1 + 10, step)
            if matr_a.get_matr()[i][1] != 0:
                y = (matr_b.get_matr()[i][0] - matr_a.get_matr()[i][0] * x) / matr_a.get_matr()[i][1]
            else:
                x = [matr_b.get_matr()[i][0] / matr_a.get_matr()[i][0] for _ in range(int((up - low) / step))]
                y = np.arange(x2 - 10, x2 + 10, step)

            text = f"{round(matr_a.get_matr()[i][0], 3)}*X1 "

            if matr_a.get_matr()[i][1] < 0:
                text += f"{round(matr_a.get_matr()[i][1], 3)}*X2 = "
            else:
                text += f"+ {round(matr_a.get_matr()[i][1], 3)}*X2 = "
            text += str(round(matr_b.get_matr()[i][0], 3))

            if i == 0:
                self.__ax.plot(x, y, color="b", label=text)
            else:
                self.__ax.plot(x, y, color="g", label=text)

        self.__ax.plot(roots[0], roots[1], marker="o", color="r")
        plt.xlabel("X1")
        plt.ylabel("X2")
        self.__ax.legend(loc="best")
