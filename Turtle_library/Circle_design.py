from turtle import*
import turtle
t=Turtle()
title("Circle")
speed(5)
t.hideturtle()
pensize(2)
for i in range(100,0,-10):
    circle(i,360)
    
turtle.exitonclick()