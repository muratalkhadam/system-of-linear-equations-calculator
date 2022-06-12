from classes.SolutionWindow import *
from constants import FONT, START_ROW_FOR_ENTRIES, DEFAULT_PICK

import random

from tkinter.ttk import Combobox


class MainWindow:
    def __init__(self, height=800, width=600, title="window", resizable=(True, True)):
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
        self.__picked_method = tk.StringVar(value=DEFAULT_PICK)

    # створрює вікно рішення
    def __solve_by_method(self, matr_a, matr_b):
        solution = SolutionWindow(self.__root, self.__picked_method.get(), matr_a, matr_b,
                                  title=self.__picked_method.get())
        solution.get_root().grab_set()
        solution.display()

    # очищає раніше створене поле коефіцієнтів
    def __clear_grid(self):
        for el in self.__frame_for_coeff.winfo_children():
            el.destroy()

    # перевіряє чи сходиться обранний метод для введеної/згенерованої матриці
    def __is_valid_method(self, matr_a, matr_b):
        if self.__picked_method.get() == "LUP-метод" or self.__picked_method.get() == "Матричний метод":
            if not matr_a.is_singular():
                self.__solve_by_method(matr_a, matr_b)
            else:
                mb.askretrycancel("Error!", "Det(A) = 0")

        if self.__picked_method.get() == "Метод Гауса-Холецького":
            if matr_a.get_determinate() > 0 and matr_a.is_simetrical():
                self.__solve_by_method(matr_a, matr_b)
            else:
                mb.askretrycancel("Error!", "Матриця повинна бути симетричною та det(A) > 0")

    # заповнює матрицю коефіцієнтів та вектор вільних членів значеннями
    def __fill_matrix(self):
        if self.__picked_method.get() != DEFAULT_PICK:
            try:
                matr = np.array([float(x.get())
                                 for x in self.__frame_for_coeff.winfo_children()
                                 if isinstance(x, tk.Entry)]) \
                    .reshape(self.__amount, self.__amount + 1)

                a = matr[:, :self.__amount]
                matr_a = Matrix(len(a), len(a[0]), a)

                b = matr[:, self.__amount:]
                matr_b = Matrix(len(b), len(b[0]), b)

                self.__is_valid_method(matr_a, matr_b)
            except ValueError:
                mb.askretrycancel("Check the input", "Поля або не заповнені, або некоректний тип введення!")
        else:
            mb.showerror("Error", "Спершу оберіть метод!")

    # створює простір для вибору методу розв'язання
    def __create_methodpick(self):
        solve_button = tk.Button(self.__root, text="Вирішити", font=FONT, command=self.__fill_matrix, background="red",
                                 relief="groove")
        solve_button.grid(row=2, column=1, columnspan=3, sticky="wesn")

        method_label = tk.Label(self.__root, text="Оберіть метод вирішення системи: ", font=FONT, background=COLOR)
        method_label.grid(row=3, column=0)

        tk.Radiobutton(self.__root, text="LUP-метод", font=FONT, variable=self.__picked_method, value="LUP-метод",
                       activebackground="orange", bg=COLOR). \
            grid(row=4, column=0, sticky="w")
        tk.Radiobutton(self.__root, text="Матричний метод", font=FONT, variable=self.__picked_method,
                       value="Матричний метод", activebackground="orange", bg=COLOR). \
            grid(row=5, column=0, sticky="w")
        tk.Radiobutton(self.__root, text="Метод Гауса-Холецького", font=FONT, variable=self.__picked_method,
                       value="Метод Гауса-Холецького", activebackground="orange", bg=COLOR). \
            grid(row=6, column=0, sticky="w")

    # створює поля коефіцієнтів в залежності від кількості невідомих
    def __create_field(self, amount):
        start_row = START_ROW_FOR_ENTRIES

        self.__clear_grid()
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
        self.__create_methodpick()

    # отримує значення кількості невідомих, перевіривши його на валідність
    def __get_amount(self):
        try:
            self.__amount = int(self.__amount_of_eq.get())
            self.__create_field(self.__amount)
        except ValueError:
            mb.showerror("Error", "Оберіть ранг системи")

    # реалізація кнопки виходу з програми
    def __exit(self):
        choice = mb.askyesno("Quit", "Ви бажаєте покинути програму?")
        if choice:
            self.__root.destroy()

    # створює та розміщає віджети на формі
    def __pack_widgets(self):
        head_label = tk.Label(self.__root, text="Калькулятор систем лінійних рівнянь", font=FONT, background=COLOR,
                              justify=tk.LEFT)
        head_label.grid(row=0, column=0, sticky="w")

        amount_label = tk.Label(self.__root, text="Кількість невідомих, яку бажаєте ввести:", font=FONT, width=70,
                                background=COLOR, justify=tk.LEFT)
        amount_label.grid(row=1, column=0, sticky="w")

        self.__amount_of_eq.grid(row=1, column=1, sticky="we")

        get_amount_button = tk.Button(self.__root, text="Створити", font=FONT, command=self.__get_amount,
                                      background=COLOR, justify=tk.RIGHT)
        get_amount_button.grid(row=1, column=3, sticky="w")

        exit_butt = tk.Button(self.__root, text="Вихід", font=FONT, command=self.__exit, background=COLOR,
                              activebackground="red")
        exit_butt.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="we")

        self.__auto_button.grid(row=1, column=2, padx=5, pady=5, sticky="we")
        self.__root.geometry("1200x250")

    # зациклення вікна
    def run(self):
        self.__pack_widgets()
        self.__root.mainloop()
