import turtle
import random
t=turtle.Turtle()
turtle.title("Spiral Design")
turtle.bgcolor("black")
t.speed(30)
t.penup()
t.right(90)
t.forward(50)
t.left(90)
colors = ["red",
          "cyan",
          "yellow",
          "purple",
          "orange",
          "pink",
          "green"
          ]
for i in range(200):
    color=random.choice(colors)
    t.pencolor(color)
    t.fillcolor(color)
    t.penup()
    t.forward(i+50)
    t.pendown()
    t.left(50)
    t.begin_fill()
    t.circle(5)
    t.end_fill()
turtle.exitonclick()