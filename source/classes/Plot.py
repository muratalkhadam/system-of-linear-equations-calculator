import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self):
        self.__fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)

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

    def get_fig(self):
        return self.__fig
    # def init(self, x_size=20):
    #     self.__fig = plt.figure(figsize=(5, 4), dpi=100, edgecolor="pink")
    #     self.__fig.subplots_adjust(top=1)
    #
    #     self.ax1 = self.__fig.add_subplot(211)
    #     self.ax1.set_title('Solution visualization')
    #
    #     self.x = np.arange(-20, 20, 0.01)
    #     self.y = self.x ** 2
    #     # self.y = np.sin(2 * np.pi * self.x)
    #
    #     self.line = self.ax1.plot(self.x, self.y, color='blue', lw=2)
    #     # Fixing random state for reproducibility
    #     np.random.seed(19680801)
    #
    # def get_fig(self):
    #     return self.__fig
    #
    # def get_x(self):
    #     return self.x
    #
    # def get_y(self):
    #     return self.y
    #
    # def set_fig(self, formula):
    #     self.__fig = formula
