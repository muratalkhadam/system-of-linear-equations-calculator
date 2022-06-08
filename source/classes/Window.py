import random

from constants import COLOR, FONT
from classes.Solution import *
from tkinter.ttk import Combobox

import tkinter.messagebox as mb


class Window:
    def __init__(self, height=800, width=600, title="window", resizable=(True, True), icon=None):
        self.__root = tk.Tk()
        self.__root.title(title)
        self.__root.resizable(resizable[0], resizable[1])
        self.__root.geometry(f"{height}x{width}")
        self.__root["bg"] = COLOR

        self.__amount_of_eq = Combobox(self.__root, values=([str(x) for x in range(2, 9)]), state="readonly", width=10)
        self.__amount = 0

        self.__is_auto = tk.BooleanVar()
        self.__auto_button = tk.Checkbutton(text="auto", variable=self.__is_auto)
        self.__frame_for_coeff = tk.Frame(self.__root, background=COLOR)
        self.__picked_method = tk.StringVar(value="-")

    def solve_by_method(self, matr_a, matr_b):
        solution = SolutionWindow(self.__root, self.__picked_method.get(), matr_a, matr_b, title=self.__picked_method.get())
        solution.get_root().grab_set()
        solution.display()

    def clear_entries(self):
        for el in self.__frame_for_coeff.winfo_children():
            if isinstance(el, tk.Entry):
                el.delete(0, tk.END)

    def on_closing(self):
        choose = mb.askokcancel("Quit", "Do you want to quit?")
        if choose:
            self.__root.destroy()

    def clear_grid(self):
        for el in self.__frame_for_coeff.winfo_children():
            el.destroy()

    def display_solution(self, matr_a, matr_b):
        if self.__picked_method.get() == "lup" or self.__picked_method.get() == "matrix":
            if matr_a.get_determinate() != 0:
                self.solve_by_method(matr_a, matr_b)
            else:
                mb.askretrycancel("Error!", "Det(A) = 0")
                # self.clear_entries()

        if self.__picked_method.get() == "gause":
            if matr_a.get_determinate() > 0 and matr_a.is_simetrical():
                self.solve_by_method(matr_a, matr_b)
            else:
                mb.askretrycancel("Error!", "Matrica doljna bit' simetrichnaya i det(A) > 0")
                # self.clear_entries()

    def solve(self):
        if self.__picked_method.get() != "-":
            # try:
            matr = np.array([float(x.get())
                             for x in self.__frame_for_coeff.winfo_children()
                             if isinstance(x, tk.Entry)])\
                .reshape(self.__amount, self.__amount + 1)

            matr_a = matr[:, :self.__amount]
            A = Matrix(len(matr_a), len(matr_a[0]), matr_a)
            matr_b = matr[:, self.__amount:]
            B = Matrix(len(matr_b), len(matr_b[0]), matr_b)

            self.display_solution(A, B)
            # except ValueError:
            #     mb.askretrycancel("Check the input", "Your entry are empty\nor\nincorrect data type given!")
        else:
            mb.showerror("Error", "Check the solution method!")

    def create_method_pick(self):
        solve_button = tk.Button(self.__root, text="SOLVE", font=FONT, command=self.solve, background="red", relief="groove")
        solve_button.grid(row=2, column=1, columnspan=3, sticky="wesn")

        method_label = tk.Label(self.__root, text="Choose the method of solution: ", font=FONT, background=COLOR)
        method_label.grid(row=3, column=0)

        tk.Radiobutton(self.__root, text="LUP-метод", font=FONT, variable=self.__picked_method, value="lup",
                       activebackground="orange", bg=COLOR).grid(row=4, column=0, sticky="w")
        tk.Radiobutton(self.__root, text="Матричний метод", font=FONT, variable=self.__picked_method, value="matrix",
                       activebackground="orange", bg=COLOR).grid(row=5, column=0, sticky="w")
        tk.Radiobutton(self.__root, text="Метод Гауса-Холецького", font=FONT, variable=self.__picked_method, value="gause",
                       activebackground="orange", bg=COLOR).grid(row=6, column=0, sticky="w")

    def create_field(self, amount):
        start_row = 2

        self.clear_grid()
        self.__frame_for_coeff.grid(row=2, column=0, sticky="we")
        self.__root.geometry("1200x450")

        index = 0
        for i in range(amount):
            for j in range(2 * amount + 1):
                if j % 2 == 0:
                    temp = tk.Entry(self.__frame_for_coeff, width=7, justify=tk.RIGHT)
                    if self.__is_auto.get():
                        number = round(random.uniform(-20, 20), 3)

                        temp.insert(0, str(number))
                        temp.configure(state="disabled")
                else:
                    index = index + 1
                    if j != 2 * amount - 1:
                        temp = tk.Label(self.__frame_for_coeff, text=f" X{index} + ")
                    else:
                        temp = tk.Label(self.__frame_for_coeff, text=f" X{index} = ")
                temp.grid(row=i + start_row, column=j, pady=2, padx=3)
            index = 0
        self.create_method_pick()

    def get_amount(self):
        try:
            self.__amount = int(self.__amount_of_eq.get())
            self.create_field(self.__amount)
        except ValueError:
            mb.showerror("Error", "Choose the rank of system!")

    def exit(self):
        choice = mb.askyesno("Quit", "Do you want to quit?")
        if choice:
            self.__root.destroy()

    def pack_widgets(self):
        head_label = tk.Label(self.__root, text="System of linear equations calculator", font=FONT, background=COLOR,
                              justify=tk.LEFT)
        head_label.grid(row=0, column=0, sticky="w")

        amount_label = tk.Label(self.__root, text="Amount of equations which you want to enter:", font=FONT, width=70,
                                background=COLOR, justify=tk.LEFT)
        amount_label.grid(row=1, column=0, sticky="w")

        self.__amount_of_eq.grid(row=1, column=1, sticky="we")

        get_amount_button = tk.Button(self.__root, text="Create", font=FONT, command=self.get_amount, background=COLOR,
                                      justify=tk.RIGHT)
        get_amount_button.grid(row=1, column=3, sticky="w")

        exit_butt = tk.Button(self.__root, text="Exit", font=FONT, command=self.exit, background=COLOR,
                              activebackground="red")
        exit_butt.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="we")

        self.__auto_button.grid(row=1, column=2, padx=5, pady=5, sticky="we")
        self.__root.geometry("1200x250")

    def run(self):
        self.pack_widgets()
        self.__root.mainloop()


if __name__ == "__main__":
    win = Window(title="MyWin")
    win.run()
