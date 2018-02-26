'''Paddle game  by: Xerex nar
using turtle module for graphics, pygame for sound'''


import turtle, random, time, math, winsound
from pygame import mixer

mixer.init()

# Setup the screen 
screen = turtle.Screen()
screen.setup(720,480)
screen.bgcolor("blue")
screen.title("X.paddle game (beta) by: Xerex nar 2/26/2018")
screen.tracer(0) # it ignore the drawing part, so it works some how in a same way as pygame.flip() method 

images = ["ball.gif","paddle.gif"] # creating a list to hold all the images, as we might expand the game later on
for image in images:
     turtle.register_shape(image) # registering the images

# registering the sound files 
ball_paddle = mixer.Sound("s_p.wav")  
ball_walls = mixer.Sound("s_w.wav") 

# this part its little bit :D ,.. i just made some functions fast to have some text here and there
# the better way is to create a class for it 
p6 = turtle.Turtle()
p6.hideturtle()
p7 = turtle.Turtle()

# this class could be done in many different ways, but it is kind a strting point 
class Life(turtle.Turtle):
     def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.pencolor("red")
        self.fillcolor("yellow")
        self.shape("square")
        self.shapesize(1,0.5)
        self.setpos(x,y)
        self.speed(0)

l1 = Life(200,200)
l2 = Life(185,200)
l3 = Life(170,200)
life_counter = 3

####################################     most of the on screen texts are here 
def game_over():
    p6.color("black")
    p6.hideturtle()
    p6.speed(1)
    p6.penup()
    font = ("arial", "20", "bold")
    p6.setpos(-50,0)
    p6.write("Game over", font = font)
    return True 

def warning():
    p6.color("black")
    p6.hideturtle()
    p6.speed(1)
    p6.penup()
    font = ("arial", "14", "bold")
    p6.setpos(-50,0)
    p6.write("One life down", font = font)
    time.sleep(1)
    p6.setpos(-50,-20)
    p6.write(str(life_counter) + " remain", font = font)
    time.sleep(1)
    p6.clear()
def level_info():
    p6.color("black")
    p6.hideturtle()
    p6.speed(1)
    p6.penup()
    font = ("arial", "14", "bold")
    p6.setpos(-100,0)
    p6.write("Bravo.. now things going to be little faster", font = font)
    time.sleep(2)
    p6.clear()
    p6.write("Ready?!!", font = font)
    time.sleep(2)
    p6.clear()
############################## Classes 

class Ball(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        #self.pencolor("red")
        #self.fillcolor("red")
        self.shape("ball.gif")
        self.shapesize(1)
        self.setpos(0,230)
        self.speed(0)
        self.speed = 0.4
        self.setheading(-90)
        self.direction = "down"
        self.levelup = "on"
     
    def update(self): # handling most part of the game logic
         # ball restrictions / movements / life warnings and some flags for ball movement 
        global life_counter
        self.forward(self.speed)
        if self.ycor() <=-250 and self.direction == "down":
            if life_counter == 3:
                self.setheading(random.choice((135,90,45)))
                self.direction = "up"
                l1.goto(500,500)
                l1.hideturtle()
                life_counter = 2
                warning()
            if life_counter == 2 and self.direction == "down": 
                self.setheading(random.choice((135,90,45)))
                self.direction = "up"
                l2.goto(500,500)
                l2.hideturtle()
                life_counter = 1
                warning()
            if life_counter == 1 and self.direction == "down":
                game_over()
            #self.setheading(random.choice((135,90,45)))
            #self.direction = "up"
        if  self.ycor() >= 230 and self.direction == "up":
            ball_walls.play()
            self.setheading(random.choice((-135,-90,-45)))
            self.direction = "down"
        if self.xcor() <= -350 or self.xcor() >= 350:
            ball_walls.play()
            self.right(45)

    def is_hit(self, other): # this part wehre we use a bit of math for collision between ball and paddle 
        a = (self.xcor() - other.xcor()) 
        b = (self.ycor() - other.ycor()) 
        distance = math.sqrt((a**2)+(b**2))
        if distance < 35:
            return True
        else:
            return False

    def level_up(self): # controlling the ball speed 
        self.speed += 0.2


class Paddle(turtle.Turtle):
    def __init__(self,x ,y= -210 ):
        turtle.Turtle.__init__(self)
        self.penup()
        #self.color("green")
        #self.fillcolor("lightgreen")
        self.shape("paddle.gif")
        self.setpos(x,-210)
        self.width = 4
        self.height = 1
        self.shapesize(1,3)
        self.speed(0)
        self.speed = 0.4
        self.direction = "stop"

    
    def update(self): # restricting the paddle and movement
        if self.xcor() >= 320:
            self.setx(320)
        if self.xcor() <= -320:
            self.setx(-320)
        if self.direction == "left":
            self.goto(self.xcor() - self.speed, self.ycor())
        elif self.direction == "right":
            self.goto(self.xcor() + self.speed, self.ycor())
        elif self.direction == "stop":
            self.goto(self.xcor(), self.ycor())

    # these functions are returning the direction        
    def left(self): 
        self.direction = "left"
    def right(self):
        self.direction = "right"
    def down(self):
        self.direction = "stop"
    def level_up(self):
        self.speed += 0.2

# instances
ball = Ball()
paddle = Paddle(0)

count = 0
def main(): #main function of the game
     # some basic logic to control the counter, levelups, and screen writing calls 
    p7.hideturtle()
    p7.penup()
    def score():
        global count, life_counter
        count += 10
        if count == 100:
            if ball.levelup == "on":
                ball.level_up()
                paddle.level_up()
                ball.levelup = "off"
                level_info()
        p7.color("black")
        p7.speed(1)
        font = ("arial", "14", "bold")
        p7.setpos(-200,200)
        p7.write("Score: "+ str(count), font = font)
        
    ##########################################
        # key bindings
    turtle.listen()
    turtle.onkey(paddle.left,"Left")
    turtle.onkey(paddle.right,"Right")
    turtle.onkey(paddle.down,"Down")

     # main flag and game loop 
    running = True
    while running:
        screen.update() # we have to use it with screen.tracer() method 
        ball.update()
        paddle.update()
        if  ball.direction == "down" and ball.is_hit(paddle): # checking the collision 
            ball_paddle.play() # collision sound 
            ball.setheading(random.choice((135,90,45)))
            ball.direction = "up" 
            p7.clear()
            score()
               
if __name__ =="__main__": # checking and calling the main function 
    main()

