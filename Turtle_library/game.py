from turtle import*
import turtle
t1=Turtle()
t2=Turtle()
ht()
t1.pencolor("blue")
t2.pencolor("red")
t1.penup()
t2.penup()
t1.speed(100)
t2.speed(100)
t1.goto(-200,0)
t2.goto(200,0)
t2.left(180)
t1.pendown()
t2.pendown()

for i in range(10):
    t1.fd(35)
    t1.penup()
    t1.fd(5)
    t1.pendown()
for j in range(40):
    for k in range(10):
        t1.undo()
        t1.undo()
        t1.undo()
        t1.undo()
        t2.fd(35)
        t2.penup()
        t2.fd(5)
        t2.pendown()
    for l in range(10):
        t2.undo()
        t2.undo()
        t2.undo()
        t2.undo()
        t1.fd(35)
        t1.penup()
        t1.fd(5)
        t1.pendown()

turtle.exitonclick()