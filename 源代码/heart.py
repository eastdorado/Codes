# Python画爱心
# 公众号：Charles的皮卡丘
import turtle
import time


def Go_to(x, y):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()


def Circle(num, size, degree):
    for i in range(num):
        turtle.forward(size)
        turtle.right(degree)


def Line(size):
    turtle.forward(51 * size)


def Heart(x, y, size):
    Go_to(x, y)
    turtle.left(150)
    turtle.begin_fill()
    Line(size)
    # Big
    Circle(num=150, size=size, degree=0.3)
    # Small
    Circle(num=210, size=size, degree=0.786)
    turtle.left(120)
    Circle(num=210, size=size, degree=0.786)
    Circle(num=150, size=size, degree=0.3)
    Line(size)
    turtle.end_fill()


def paint(a, b):
    turtle.right(a)
    turtle.forward(b)


def arrow():
    turtle.pensize(10)
    turtle.setheading(0)
    Go_to(-400, 0)
    turtle.left(15)
    turtle.forward(150)
    Go_to(339, 178)
    turtle.forward(150)
    turtle.pensize(1)
    turtle.color('red', 'red')
    turtle.begin_fill()
    turtle.left(120)
    turtle.forward(20)
    paint(150, 35)
    paint(120, 35)
    paint(150, 20)
    turtle.end_fill()


def draw():
    turtle.setup(1050, 600, 0, 0)
    # turtle.getscreen().tracer(30, 0)
    turtle.pensize(2)
    turtle.speed(10)
    turtle.color('red', 'pink')
    Heart(200, 0, 1)
    turtle.setheading(0)
    Heart(-80, -100, 1.5)
    arrow()
    turtle.done()


if __name__ == '__main__':
    draw()