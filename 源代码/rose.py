# Python画玫瑰
# 公众号：Charles的皮卡丘
import turtle
import time


class rose1:
    def __init__(self):
        print('[INFO]:Rose1 class...')

    def paint(self, angle1, r, angle2):
        turtle.penup()
        turtle.setheading(angle1)
        turtle.pendown()
        turtle.circle(r, angle2)

    def draw(self):
        turtle.speed(9)
        turtle.color("white")
        turtle.pensize(7)
        turtle.penup()
        turtle.goto(50, -50)
        turtle.pendown()
        turtle.dot(200, 'pink')
        turtle.penup()
        turtle.goto(50, 86.6)
        angle1 = -150
        r = 300
        angle2 = 46
        for j in range(21):
            self.paint(angle1, r, angle2)
            angle2 -= 25
            self.paint(angle1 + angle2 + 25, r, -angle2)
            angle2 += 25
            angle1 += 66
            r = 0.9 * r
        turtle.done()


class rose2:
    def __init__(self):
        print('[INFO]:Rose2 class...')

    def paint(self, num, a, b):
        for i in range(num):
            turtle.fd(a)
            turtle.left(b)

    def draw(self):
        turtle.setup(600, 800, 0, 0)
        turtle.penup()
        turtle.seth(90)
        turtle.fd(340)
        turtle.seth(0)
        turtle.pendown()
        turtle.speed(9)
        turtle.begin_fill()
        turtle.fillcolor('red')
        turtle.circle(50, 30)
        self.paint(10, 1, 10)
        turtle.circle(40, 40)
        self.paint(6, 1, 3)
        turtle.circle(80, 40)
        self.paint(20, 0.5, 5)
        turtle.circle(80, 45)
        self.paint(10, 2, 1)
        turtle.circle(80, 25)
        self.paint(20, 1, 4)
        turtle.circle(50, 50)
        time.sleep(0.1)
        turtle.circle(120, 55)
        turtle.seth(-90)
        turtle.fd(70)
        turtle.right(150)
        turtle.fd(20)
        turtle.left(140)
        turtle.circle(140, 90)
        turtle.left(30)
        turtle.circle(160, 100)
        turtle.left(130)
        turtle.fd(25)
        turtle.penup()
        turtle.right(150)
        turtle.circle(40, 80)
        turtle.pendown()
        turtle.left(115)
        turtle.fd(60)
        turtle.penup()
        turtle.left(180)
        turtle.fd(60)
        turtle.pendown()
        turtle.end_fill()
        turtle.right(120)
        turtle.circle(-50, 50)
        turtle.circle(-20, 90)
        turtle.fd(75)
        turtle.circle(90, 110)
        turtle.penup()
        turtle.left(162)
        turtle.fd(185)
        turtle.left(170)
        turtle.pendown()
        turtle.circle(200, 10)
        turtle.circle(100, 40)
        turtle.circle(-52, 115)
        turtle.left(20)
        turtle.circle(100, 20)
        turtle.circle(300, 20)
        turtle.fd(250)
        turtle.penup()
        turtle.left(180)
        turtle.fd(250)
        turtle.circle(-300, 7)
        turtle.right(80)
        turtle.circle(200, 5)
        turtle.pendown()
        turtle.left(60)
        turtle.begin_fill()
        turtle.fillcolor('green')
        turtle.circle(-80, 100)
        turtle.right(90)
        turtle.fd(10)
        turtle.left(20)
        turtle.circle(-63, 127)
        turtle.end_fill()
        turtle.penup()
        turtle.left(50)
        turtle.fd(20)
        turtle.left(180)
        turtle.pendown()
        turtle.circle(200, 25)
        turtle.penup()
        turtle.right(150)
        turtle.fd(180)
        turtle.right(40)
        turtle.pendown()
        turtle.begin_fill()
        turtle.fillcolor('green')
        turtle.circle(-100, 80)
        turtle.right(150)
        turtle.fd(10)
        turtle.left(60)
        turtle.circle(-80, 98)
        turtle.end_fill()
        turtle.penup()
        turtle.left(60)
        turtle.fd(13)
        turtle.left(180)
        turtle.pendown()
        turtle.circle(-200, 23)
        turtle.done()


if __name__ == '__main__':
    rose1().draw()
    # rose2().draw()
