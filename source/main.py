from constants import HEIGHT, WIDTH
from classes.Window import Window


def main():
    win = Window(title="System of linear equations calculator", height=HEIGHT, width=WIDTH)
    win.run()


if __name__ == "__main__":
    main()
