import tkinter 
from random import randint
root = tkinter.Tk()
root.title("Дождь")

canvas = tkinter.Canvas(root, width=1000, height=1000,bg= "gray")
canvas.pack()
Rain = []

kf = 1.5  # коэффициент изменение длины капель
min_len = 5
max_len = 15

class Drops:
    def __init__(self, canvas, width, height, x, y, yspeed, length, width_line):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.yspeed = yspeed
        self.length = length
        self.line = canvas.create_line(self.x, self.y + self.length, self.x, self.y,fill="white", width=width_line)

    def moving(self):
        self.y += self.yspeed
        self.canvas.move(self.line, 0, self.yspeed)

        # Если выходит за границы canvas
        if self.y > self.height:
            self.canvas.move(self.line, 0, -(self.height + self.length))
            self.y -= self.height + self.length


for i in range(100):
    #генерация капель
    length = randint(min_len, max_len) * kf
    width_line = 0.09 * length
    
    if length > 14:
        Rain.append(Drops(canvas, 1000, 1000, x=randint(0, 1000), y=randint(0, 1000), yspeed=randint(5, 10),
                              length=length,
                              width_line=width_line))
    else :
        Rain.append(Drops(canvas, 1000, 1000, x=randint(0, 1000), y=randint(0, 1000), yspeed=randint(3, 6),
                              length=length,
                              width_line=width_line))

def animation():
    for drop in Rain:
        drop.moving()

    root.after(1, animation)
  
animation()
root.mainloop()