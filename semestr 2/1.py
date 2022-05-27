from tkinter import *
from math import *

speed = int(input('Введите скорость, с которой будет двигаться точка: '))
direction = input('Введите направление ')
root = Tk()
Canv = Canvas(root, width = 600, height = 600, bg = 'yellow')
Canv.pack()
circle = Canv.create_oval(100, 100, 500, 500,  fill = 'black')
dot = Canv.create_oval(275, 75,325,125, fill = 'green')
def move(angle):
    if angle >= 360:
        angle = 0
    x = 200* cos(radians(angle))
    y = 200* sin(radians(angle))
    if direction.lower() == 'против часовой':
        angle-=3

    #по часовой - команда для движения по часовой по часовой
    if direction.lower() == 'по часовой':
        angle+=3
    #против часовой - команда для движения против часовой

    Canv.coords(dot, 275+x, 275+y, 275+x+50, 275+y+50)
    root.after(speed, move, angle)
def end(event):
    if event.keysym == 'space':
        root.destroy()
root.after(10, move, 0)
root.bind('<KeyPress>', end)
root.mainloop()
