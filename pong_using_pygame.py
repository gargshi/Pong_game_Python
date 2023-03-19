import random

import pygame, sys

# mixer init
pygame.mixer.pre_init(44100,-16,2,512) #for slow computers

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
INIT_BALL_SPD_X = 5
INIT_BALL_SPD_Y = 5
BALL_SPEED_X = INIT_BALL_SPD_X
BALL_SPEED_Y = INIT_BALL_SPD_Y
PADDLE_SPEED = 0
PADDLE_SPEED_STEP = 8
OPPONENT_SPEED = 8  ### opponent ai paddle speed
PLAYER_SCORE = 0
OPPONENT_SCORE = 0
SCOREBOARD_FONT = pygame.font.SysFont("Consolas", 30)
TIMER_FONT = pygame.font.SysFont("Consolas", 50)

SCORE_TIME = True

#sounds
HIT_SOUND=pygame.mixer.Sound("sounds/pong.ogg")
SCORE_SOUND=pygame.mixer.Sound("sounds/score.ogg")




BALL_SPEED_X *= random.choice((1, -1))
BALL_SPEED_Y *= random.choice((1, -1))


def ball_motion(BALL_SPEED_X, BALL_SPEED_Y):
    global PLAYER_SCORE, OPPONENT_SCORE, SCORE_TIME
    # moving the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y
    # collisions
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:  # vertical boundary
        pygame.mixer.Sound.play(HIT_SOUND)
        BALL_SPEED_Y *= -1
    if ball.left <= 0:  # horizontal boundary
        pygame.mixer.Sound.play(SCORE_SOUND)
        # BALL_SPEED_X *= -1 # uncomment for normal boring gameplay...
        PLAYER_SCORE += 1
        SCORE_TIME = pygame.time.get_ticks()

    if ball.right >= SCREEN_WIDTH:  # horizontal boundary
        # BALL_SPEED_X *= -1 # uncomment for normal boring gameplay...
        pygame.mixer.Sound.play(SCORE_SOUND)
        OPPONENT_SCORE += 1
        SCORE_TIME = pygame.time.get_ticks()

    if ball.colliderect(player) and BALL_SPEED_X > 0:
        pygame.mixer.Sound.play(HIT_SOUND)
        if abs(ball.right-player.left)<10:
            BALL_SPEED_X *= -1
        elif abs(ball.bottom-player.top) < 10 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.top-player.bottom) < 10 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1
    if ball.colliderect(opponent) and BALL_SPEED_X < 0:
        pygame.mixer.Sound.play(HIT_SOUND)
        if abs(ball.left-opponent.right)<10:
            BALL_SPEED_X *= -1
        elif abs(ball.bottom-opponent.top) < 10 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.top-opponent.bottom) < 10 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1
    return BALL_SPEED_X, BALL_SPEED_Y


def ball_reset(BALL_SPEED_X, BALL_SPEED_Y):
    global SCORE_TIME
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    CURRENT_TIME = pygame.time.get_ticks()  # current_instantaneous time

    time_offset_ms = 1000
    init_time = 0
    counter_steps = 3

    while counter_steps != 0:
        if init_time < (CURRENT_TIME - SCORE_TIME) < (init_time + time_offset_ms):
            no_3 = TIMER_FONT.render(f"{counter_steps}", True, light_grey)
            screen.blit(no_3, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10))
        init_time += time_offset_ms
        counter_steps -= 1

    if CURRENT_TIME - SCORE_TIME < init_time:
        BALL_SPEED_X, BALL_SPEED_Y = 0, 0
    else:
        BALL_SPEED_X = INIT_BALL_SPD_X * random.choice((1, -1))
        BALL_SPEED_Y = INIT_BALL_SPD_Y * random.choice((1, -1))
        SCORE_TIME = None
    return BALL_SPEED_X, BALL_SPEED_Y


def player_movement():
    player.y += PADDLE_SPEED
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_movement_ai():
    # dif_fact=random.choice((OPPONENT_SPEED,0))
    dif_fact = 0
    if opponent.top + dif_fact < ball.y:
        opponent.top += OPPONENT_SPEED
    if opponent.bottom - dif_fact > ball.y:
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

    # logic for game
    BALL_SPEED_X, BALL_SPEED_Y = ball_motion(BALL_SPEED_X, BALL_SPEED_Y)  # function call for ball movement
    player_movement()  # function call for player paddle movement
    opponent_movement_ai()  # function call for AI

    # draw the shapes
    screen.fill(bg_col)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    if SCORE_TIME:
        BALL_SPEED_X, BALL_SPEED_Y = ball_reset(BALL_SPEED_X, BALL_SPEED_Y)

    # rendering the scores (use another surface for the same then render it on the screen.)
    player_text = SCOREBOARD_FONT.render(f"{PLAYER_SCORE}", True, light_grey)
    opponent_text = SCOREBOARD_FONT.render(f"{OPPONENT_SCORE}", True, light_grey)
    screen.blit(player_text, (700, 0))
    screen.blit(opponent_text, (650, 0))

    pygame.display.flip()
    clock.tick(60)
