import turtle
screen = turtle.Screen()
screen.setup(500, 600, startx = 0, starty =450)

squary = turtle.Turtle()
squary.speed(0)


for i in range(1500):
    turtle.forward(i)
    turtle.left(91)

turtle.hideturtle()
turtle.done()
