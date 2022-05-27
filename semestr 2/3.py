from tkinter import Tk, Canvas
import random


def f1(x, y):
    x = 0
    y = 0.16 * y
    return x, y


def f2(x, y):
    x = 0.7 * x + 0.035 * y
    y = -0.04 * x + 0.8 * y + 1.6

    return x, y


def f3(x, y):
    x = 0.20 * x - 0.29 * y
    y = 0.23 * x + 0.22 * y + 1.6

    return x, y


def f4(x, y):
    x = -0.2 * x + 0.28 * y
    y = 0.26 * x + 0.25 * y + 0.44

    return x, y


def esc(event):
    root.destroy()


root = Tk()
root.bind('<Escape>', esc)

W = 700  # ширина
H = 500 # высота


c = Canvas(root, width=W, height=H, bg='black')
c.pack()


def main():
    x = 0
    y = 0
    flag = 0 # (0, 1)
    for _ in range(200):
        if flag == 0:
            c.create_oval(W/2+(55*x), H - (35*y), W/2 +
                        (55*x), H - (35*y), width=0, fill='green')
        elif flag == 1:
            c.create_oval(W/2-(55*x), H - (35*y), W/2 -
                        (55*x), H - (35*y), width=0, fill='green')

        rand = random.random() #случайное число от 0 до 1(вероятность)
        
        if rand < 0.4:
            x, y = f1(x, y)
        elif rand < 0.81:
            x, y = f2(x, y)
        elif rand < 0.89:
            x, y = f3(x, y)
        else:
            x, y = f4(x, y)

    root.after(100, main) #скорость отрисовки овалов


if __name__ == "__main__":
    main()
    root.mainloop()
