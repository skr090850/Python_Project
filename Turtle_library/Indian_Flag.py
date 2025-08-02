from turtle import*
import turtle
t=Turtle()
bgcolor("skyblue")
title("Indian Flag")
speed(3)
pensize(2)
t.hideturtle()

penup()
goto(-100,150)
pendown()
for j in range(3):
    begin_fill()
    if j == 0:
        color("orange")
    elif j == 1:
        color("white")
    elif j == 2:
        color("green")
    for i in range(2):
        forward(200)
        right(90)
        forward(50)
        right(90)
    end_fill()
    if j==0:
        fillcolor("orange")
    elif j==2:
        fillcolor("white")
    elif j==2:
        fillcolor("green")
    left(90)
    backward(50)
    right(90)

# for circle
penup()
goto(0,51)
pendown()
color("blue")
circle(25,360)
pensize()
penup()
goto(0,75)
pendown()
right(90)
for i in range(24):
    forward(25)
    backward(25)
    left(15)

# for stand
penup()
goto(-100,150)
pendown()
right(90)
color("brown")
begin_fill()
for k in range(2):
    forward(5)
    left(90)
    forward(700)
    left(90)
end_fill()
fillcolor("brown")

begin_fill()
color("yellow")
right(90)
circle(5,360)
end_fill()
fillcolor("yellow")
turtle.exitonclick()
# Thank you

