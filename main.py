import turtle

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 650
PADDLE_MOVE_LIMIT= SCREEN_HEIGHT // 2 #- 72
left_player = 0
right_player = 0
screen_1 = turtle.Screen()
screen_1.title("PONG")
screen_1.bgcolor('black')
screen_1.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)


def draw_ball():
    hit_ball = turtle.Turtle()
    hit_ball.speed(45)
    hit_ball.shape("circle")
    hit_ball.color("White")
    hit_ball.penup()
    hit_ball.goto(0, 0)
    hit_ball.dx = 5
    hit_ball.dy = -5
    return hit_ball


def draw_left_paddle():
    left_paddle = turtle.Turtle()
    left_paddle.speed(0)
    left_paddle.shape("square")
    left_paddle.color("orange")
    left_paddle.shapesize(stretch_wid=6, stretch_len=2)
    left_paddle.penup()
    left_paddle.goto(-400, 0)
    return left_paddle


def draw_right_paddle():
    right_paddle = turtle.Turtle()
    right_paddle.speed(0)
    right_paddle.shape("square")
    right_paddle.color("light blue")
    right_paddle.shapesize(stretch_wid=6, stretch_len=2)
    right_paddle.penup()
    right_paddle.goto(400, 0)
    return right_paddle


def paddle_L_up(): #left paddle up
    y = left_paddle.ycor()
    y = y if y < PADDLE_MOVE_LIMIT else PADDLE_MOVE_LIMIT
    y += 20
    left_paddle.sety(y)


def paddle_L_down(): #left paddle down
    y = left_paddle.ycor()
    y = y if y > -PADDLE_MOVE_LIMIT else -PADDLE_MOVE_LIMIT
    y -= 20
    left_paddle.sety(y)


def paddle_R_up(): #right paddle up
    y = right_paddle.ycor()
    y = y if y < PADDLE_MOVE_LIMIT else PADDLE_MOVE_LIMIT
    y += 20
    right_paddle.sety(y)


def paddle_R_down(): #right paddle down
    y = right_paddle.ycor()
    y = y if y > -PADDLE_MOVE_LIMIT else -PADDLE_MOVE_LIMIT
    y -= 20
    right_paddle.sety(y)


hit_ball = draw_ball()
left_paddle = draw_left_paddle()
right_paddle = draw_right_paddle()

# scoreboard
sketch_1 = turtle.Turtle()
sketch_1.speed(0)
sketch_1.color("white")
sketch_1.penup()
sketch_1.hideturtle()
sketch_1.goto(0, 260)
sketch_1.write("Left Player : 0    Right Player: 0", align="center", font=("Consolas", 20, "normal"))

#key bindings
screen_1.listen()
screen_1.onkeypress(paddle_L_up, "r")
screen_1.onkeypress(paddle_L_down, "c")
screen_1.onkeypress(paddle_R_up, "Up")
screen_1.onkeypress(paddle_R_down, "Down")

while True:
    # print(screen_1.window_height())
    screen_1.update()
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1
    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch_1.clear()
        sketch_1.write("Left_player : {}    Right_player: {}".format(left_player, right_player), align="center",font=("Courier", 24, "normal"))

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch_1.clear()
        sketch_1.write("Left_player : {}    Right_player: {}".format(left_player, right_player), align="center",font=("Courier", 24, "normal"))

        # Collision of ball and paddles
    if (hit_ball.xcor() > 360 and
        hit_ball.xcor() < 370) and (hit_ball.ycor() < right_paddle.ycor() + 40 and
                                    hit_ball.ycor() > right_paddle.ycor() - 40):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -360 and
        hit_ball.xcor() > -370) and (hit_ball.ycor() < left_paddle.ycor() + 40 and
                                     hit_ball.ycor() > left_paddle.ycor() - 40):
        hit_ball.setx(-360)
        hit_ball.dx *= -1
