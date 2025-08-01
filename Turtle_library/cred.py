import turtle
t=turtle.Turtle()
turtle.Screen().bgcolor("black")
t.width(10)
t.color("White")
t.hideturtle()
t.penup()
t.goto(-166,100)
t.pendown()

# Outer Design
t.forward(256)
t.right(90)
t.forward(220)
t.right(60)
t.forward(150)
t.right(60)
t.forward(150)
t.right(60)
t.forward(220)
#end

t.right(180)
t.penup()
t.forward(40)
t.left(90)
t.forward(40)

# 1st inner design
t.forward(40)
t.pendown()
t.forward(136)
t.right(90)
t.forward(50)
t.penup()
t.forward(40)
t.pendown()
t.forward(60)
t.right(60)
t.forward(101)
t.right(60)
t.forward(101)
t.right(60)
t.forward(110)

#2nd inner Design
t.right(90)
t.forward(136)
t.right(90)
t.penup()
t.forward(90)
t.pendown()
t.right(60)
t.forward(57)
t.right(60)
t.forward(57)
t.right(60)
t.forward(40)

# for text
t.penup()
t.right(90)
t.forward(10)
t.goto(-166,-300)
t.pendown()
t.write("CRED",font=("Arial",70,"normal"))

turtle.exitonclick()
