import pygame
import random
import numpy as np
from pyparsing import col
import serial
import time
from threading import Thread
import random


def start_flappy_bird():
    # Initialize pygame
    pygame.init()

    # Set up display
    width, height = 255, 255
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")

    # Set up clock
    clock = pygame.time.Clock()
    tick_rate = 15

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)

    # Game variables
    bird_x, bird_y = 30, height // 2
    bird_radius = 10
    bird_speed_y = 0
    gravity = 1.8
    jump_strength = -10

    pipe_width = 40
    pipe_gap = 80
    pipe_speed = 7
    pipe_list = []
    pipe_spawn_rate = tick_rate * 3  
    pipe_tick = 0

    score = 0
    font = pygame.font.Font(None, 74)
    game_over_font = pygame.font.Font(None, 50)

    # Function to create new pipes
    def create_pipe():
        pipe_height = random.randint(20, height - pipe_gap - 20)
        top_pipe = pygame.Rect(width, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(width, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap)
        return top_pipe, bottom_pipe

    # Main game loop
    running = True
    game_over = False

    # Create initial pipes
    pipe_list.append(create_pipe())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bird_speed_y = jump_strength

        if not game_over:
            # Bird movement
            bird_speed_y += gravity
            bird_y += bird_speed_y

            # Check for collision with ground or ceiling
            if bird_y - bird_radius <= 0 or bird_y + bird_radius >= height:
                game_over = True

            # Pipe movement
            for pipe in pipe_list:
                pipe[0].x -= pipe_speed
                pipe[1].x -= pipe_speed

            # Remove pipes that move off screen
            if len(pipe_list) > 0 and pipe_list[0][0].right < 0:
                pipe_list.pop(0)
                score += 1

            pipe_tick += 1
            if (pipe_tick == pipe_spawn_rate):
                pipe_tick = 0
                pipe_list.append(create_pipe())

            # Check for collision with pipes
            for pipe in pipe_list:
                if bird_x + bird_radius > pipe[0].left and bird_x - bird_radius < pipe[0].right:
                    if bird_y - bird_radius < pipe[0].bottom or bird_y + bird_radius > pipe[1].top:
                        game_over = True

    
        # Actual coordinates to draw
        to_send = []
        add_bird_coords(to_send, bird_x, bird_y, bird_radius, 50, 255)
        
        for pipe in pipe_list:
            add_top_pipe_coords(to_send, pipe[0], 255)
            add_bottom_pipe_coords(to_send, pipe[1], 255)


        if DRAW_WALLS:
            # Bottom Wall
            for _ in range(0, LASER_ON_DELAY):
                add_coord(to_send, 255, 255, 0)

            for i in range(255, -1, -5):
                add_coord(to_send, i, 255, 255)

            for _ in range(0, LASER_OFF_DELAY):
                add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])

            # Top Wall
            for _ in range(0, LASER_ON_DELAY):
                add_coord(to_send, 0, 0, 0)

            for i in range(0, 256, 5):
                add_coord(to_send, i, 0, 255)

            for _ in range(0, LASER_OFF_DELAY):
                add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])


        to_send.extend([13,13,13])
        print(len(to_send))
        # serialPort.write(bytearray(list(to_send)))


        # Clear the screen
        screen.fill(black)

        # Draw bird
        pygame.draw.circle(screen, yellow, (bird_x, bird_y), bird_radius)

        # Draw pipes
        for pipe in pipe_list:
            pygame.draw.rect(screen, green, pipe[0])
            pygame.draw.rect(screen, green, pipe[1])

        # Draw score
        score_text = font.render(str(score), True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

        # Check game over
        if game_over:
            game_over_text = game_over_font.render("Game Over", True, white)
            screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

        # Update display
        pygame.display.flip()

        # Frame rate
        clock.tick(tick_rate)

    pygame.quit()


def add_top_pipe_coords(coords:list, pipe:pygame.Rect, colour):
    x_left, y_top = pipe.topleft
    x_right, y_bot = pipe.bottomright

    incr = 5

    for _ in range(0, LASER_ON_DELAY):
        add_coord(coords, x_left, y_top, 0)

    for y in range(y_top+incr, y_bot+1, incr):
        add_coord(coords, x_left, y, colour)

    if (coords[-2] != y_bot):
        add_coord(coords, x_left, y_bot, colour)

    for x in range(x_left+incr, x_right+1, incr):
        add_coord(coords, x + incr, y_bot, colour)

    if (coords[-3] != x_right):
        add_coord(coords, x_right, y_bot, colour)

    for y in range(y_bot+incr,y_top-1, -incr):
        add_coord(coords, x_right, y, colour)

    if (coords[-2] != y_top):
        add_coord(coords, x_right, y_top, colour)

    for _ in range(0, LASER_OFF_DELAY):
        add_coord(coords, x_right, y_top, colour)


def add_bottom_pipe_coords(coords:list, pipe:pygame.Rect, colour):
    x_left, y_top = pipe.topleft
    x_right, y_bot = pipe.bottomright

    incr = 5

    for _ in range(0, LASER_ON_DELAY):
        add_coord(coords, x_left, y_bot, 0)

    for y in range(y_bot+incr,y_top-1, -incr):
        add_coord(coords, x_left, y, colour)

    if (coords[-2] != y_top):
        add_coord(coords, x_right, y_top, colour)
    
    for x in range(x_left+incr, x_right+1, incr):
        add_coord(coords, x + incr, y_top, colour)

    if (coords[-3] != x_right):
        add_coord(coords, x_right, y_top, colour)
    
    for y in range(y_top+incr, y_bot+1, incr):
        add_coord(coords, x_right, y, colour)

    if (coords[-2] != y_bot):
        add_coord(coords, x_right, y_bot, colour)

    for _ in range(0, LASER_OFF_DELAY):
        add_coord(coords, x_right, y_bot, colour)

    

def add_bird_coords(coords:list, x_center, y_center, radius, num_points, colour):
    # Generate angles evenly spaced around the circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

    first = True
    first_x = 0
    first_y = 0

    for angle in angles:
        # Calculate the x and y coordinates of the points
        x = int(round(x_center + radius * np.cos(angle)))
        y = int(round(y_center + radius * np.sin(angle)))

        if (x >= 0 and x <= 255 and y >= 0 and y <= 255):

            if (first):
                for _ in range(0, LASER_ON_DELAY):
                    add_coord(coords, x, y, 0)
                first_x = x
                first_y = y
                first = False
                
            add_coord(coords, x, y, colour)

    for _ in range(0, LASER_OFF_DELAY):
        add_coord(coords, first_x, first_y, colour)

def add_coord(coords:list, x, y, colour):

    if (y > 255):
        y = 255
    elif (y < 0):
        y = 0
    
    if (x > 255):
        x = 255
    elif (x < 0):
        x = 0

    if (colour > 255):
        colour = 255
    elif ( colour < 0):
        colour = 0
    
    coords.append(x)
    coords.append(y)
    coords.append(colour)

# init serial
# serialPort = serial.Serial(
#     port="COM4", baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
# )

# def readSerial():
#     successes = 0
#     while 1:
#     # Read data out of the buffer until a carraige return / new line is found
#         #serialString = serialPort.read_until(expected="\n", size=10)

#         serialString = serialPort.readline()
#         if serialString:
#             try:
#                 print(serialString.decode("ascii"))
#             except:
#                 print(serialString)


# readThread = Thread(target = readSerial)
# readThread.daemon = True 
# readThread.start()

LASER_ON_DELAY = 10         # Point delay before turning the laser back on
LASER_OFF_DELAY = 5         # Point delay before turning the laser off
DRAW_WALLS = True


start_flappy_bird()