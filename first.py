import turtle

myT =None

myT =turtle.Turtle()
myT.shape('circle')

for i in range(0,8):
    myT.forward(200)
    myT.right(45)

turtle.done()