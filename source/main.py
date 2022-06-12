from constants import HEIGHT, WIDTH
from classes.MainWindow import MainWindow


def main():
    win = MainWindow(title="System of linear equations calculator", height=HEIGHT, width=WIDTH)
    win.run()


if __name__ == "__main__":
    main()
