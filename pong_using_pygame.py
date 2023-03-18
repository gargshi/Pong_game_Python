import random

import pygame, sys

# initialise
pygame.init()
clock = pygame.time.Clock()

# GLOBAL CONTROL VARIABLES
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
BALL_DIAMETER = 25
PADDLE_LENGTH = 140
PADDLE_WIDTH = 10
OFFSET = 20
OFFSET_OPPONENT = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
PADDLE_SPEED = 0
PADDLE_SPEED_STEP = 8
OPPONENT_SPEED = 20 ### opponent ai paddle speed
PLAYER_SCORE=0
OPPONENT_SCORE=0
SCOREBOARD_FONT=pygame.font.SysFont("Arial",30)

BALL_SPEED_X *= random.choice((1,-1))
BALL_SPEED_Y *= random.choice((1,-1))

def ball_motion(BALL_SPEED_X, BALL_SPEED_Y):
    # moving the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y
    # collisions
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:  # vertical boundary
        BALL_SPEED_Y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:  # horizontal boundary
        #BALL_SPEED_X *= -1 # uncomment for normal boring gameplay...
        BALL_SPEED_X,BALL_SPEED_Y = ball_reset(BALL_SPEED_X,BALL_SPEED_Y)
    if ball.colliderect(player) or ball.colliderect(opponent):
        BALL_SPEED_X *= -1
    return BALL_SPEED_X, BALL_SPEED_Y

def ball_reset(BALL_SPEED_X,BALL_SPEED_Y):
    ball.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    BALL_SPEED_X *= random.choice((1, -1))
    BALL_SPEED_Y *= random.choice((1, -1))
    return BALL_SPEED_X,BALL_SPEED_Y


def player_movement():
    player.y += PADDLE_SPEED
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_movement_ai():
    if opponent.top < ball.y:
        opponent.top += OPPONENT_SPEED
    if opponent.bottom > ball.y:
        opponent.bottom -= OPPONENT_SPEED
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PONG_USING_PYGAME')

# draw rectangles/shapes
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_DIAMETER / 2, SCREEN_HEIGHT / 2 - BALL_DIAMETER / 2, BALL_DIAMETER,
                   BALL_DIAMETER)
player = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH - 10, SCREEN_HEIGHT / 2 - PADDLE_LENGTH / 2, PADDLE_WIDTH,
                     PADDLE_LENGTH)
opponent = pygame.Rect(PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_LENGTH / 2, PADDLE_WIDTH, PADDLE_LENGTH)

# colors
bg_col = pygame.Color('grey12')
light_grey = (250, 250, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                PADDLE_SPEED += PADDLE_SPEED_STEP
            if event.key == pygame.K_UP:
                PADDLE_SPEED -= PADDLE_SPEED_STEP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                PADDLE_SPEED -= PADDLE_SPEED_STEP
            if event.key == pygame.K_UP:
                PADDLE_SPEED += PADDLE_SPEED_STEP

    #logic for game
    BALL_SPEED_X, BALL_SPEED_Y = ball_motion(BALL_SPEED_X, BALL_SPEED_Y)  # function call for ball movement
    player_movement()  # function call for player paddle movement
    opponent_movement_ai() # function call for AI

    # draw the shapes
    screen.fill(bg_col)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    #rendering the scores (use another surface for the same then render it on the screen.)
    player_text = SCOREBOARD_FONT.render(f"{PLAYER_SCORE}", True, light_grey)
    opponent_text = SCOREBOARD_FONT.render(f"{OPPONENT_SCORE}", True, light_grey)
    screen.blit(player_text, (700, 0))
    screen.blit(opponent_text, (650, 0))


    pygame.display.flip()
    clock.tick(60)