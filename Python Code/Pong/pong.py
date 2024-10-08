import pygame
import random
import numpy as np
import serial
import time
from threading import Thread
import random

def start_pong_game():
    # Initialize pygame
    pygame.init()

    # Set up the screen
    width, height = 255, 255
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong Game")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Ball settings
    default_ball_speed = 4
    ball_radius = 5
    ball_velocity_x = default_ball_speed * random.choice((1, -1))
    ball_velocity_y = 0.1
    ball_x, ball_y = width // 2, height // 2

    # Paddle settings
    paddle_width, paddle_height = 10, 50
    paddle_velocity = 7
    player_one_x, player_one_y = 10, height // 2 - paddle_height // 2
    player_two_x, player_two_y = width - 10 - paddle_width, height // 2 - paddle_height // 2

    # Scores
    player_score, opponent_score = 0, 0
    font = pygame.font.Font(None, 74)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_one_y > 0:
            player_one_y -= paddle_velocity

            if (player_one_y < 0):
                player_one_y = 0

        if keys[pygame.K_s] and player_one_y < height - paddle_height:
            player_one_y += paddle_velocity

            if (player_one_y > height - paddle_height):
                player_one_y = height - paddle_height

        if keys[pygame.K_UP] and player_two_y > 0:
            player_two_y -= paddle_velocity

            if (player_two_y < 0):
                player_two_y = 0

        if keys[pygame.K_DOWN] and player_two_y < height - paddle_height:
            player_two_y += paddle_velocity

            if (player_two_y > height - paddle_height):
                player_two_y = height - paddle_height

        # Ball movement
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y

        # Ball collision with top and bottom walls
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
            ball_velocity_y = -ball_velocity_y

        # Ball collision with paddles
        if (ball_x - ball_radius <= player_one_x + paddle_width and player_one_y <= ball_y <= player_one_y + paddle_height):
            if (ball_velocity_x < 0) :
                ball_velocity_x -= 1
            else :
                ball_velocity_x += 1
            ball_velocity_x *= -1

            paddle_y_intersect = player_one_y + paddle_height / 2 - ball_y
            normalized_intersect = paddle_y_intersect / (paddle_height / 2)
            bounce_angle = normalized_intersect * 5 * np.pi / 12

            ball_velocity_y = np.abs(ball_velocity_x) * -np.sin(bounce_angle)

            ball_x = player_one_x + paddle_width  + ball_radius

        elif (ball_x + ball_radius >= player_two_x and player_two_y <= ball_y <= player_two_y + paddle_height):
            if (ball_velocity_x < 0) :
                ball_velocity_x -= 1
            else :
                ball_velocity_x += 1
            ball_velocity_x *= -1

            paddle_y_intersect = player_two_y + paddle_height / 2 - ball_y
            normalized_intersect = paddle_y_intersect / (paddle_height / 2)
            bounce_angle = normalized_intersect * 5 * np.pi / 12

            ball_velocity_y = np.abs(ball_velocity_x) * -np.sin(bounce_angle)

            ball_x = player_two_x - ball_radius

        # Ball out of bounds
        if ball_x < 0:
            opponent_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_velocity_x = default_ball_speed * random.choice((1, -1))
            ball_velocity_y = 0
        if ball_x > width:
            player_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_velocity_x = default_ball_speed * random.choice((1, -1))
            ball_velocity_y = 0
        
        # Actual coordinates to draw
        to_send = []
        add_paddle_coords(to_send, player_one_x, player_one_y, paddle_width, paddle_height, 100, 255, False)

        add_ball_coords(to_send, ball_x, ball_y, ball_radius, 50, 255)
        
        add_paddle_coords(to_send, player_two_x, player_two_y, paddle_width, paddle_height, 100, 255, True)

        if DELAYS:
            # Pause Drawing at end to try and reduce streaks
            for _ in range(0, DELAY_LENGTH):
                to_send.extend([128, 128, 0]) 

        to_send.extend([13,13,13,13,13,13])
        print(len(to_send))
        serialPort.write(bytearray(list(to_send)))

        # Pygame Stuff
        # Clear screen
        screen.fill(black)

        # Draw ball
        pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

        # Draw paddles
        pygame.draw.rect(screen, white, (player_one_x, player_one_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, white, (player_two_x, player_two_y, paddle_width, paddle_height))

        # Draw scores
        player_text = font.render(str(player_score), True, white)
        screen.blit(player_text, (width // 4, 20))
        opponent_text = font.render(str(opponent_score), True, white)
        screen.blit(opponent_text, (3 * width // 4, 20))

        # Refresh the screen
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(15)

    # Quit pygame
    pygame.quit()

# Paddles to Coordinates
def add_paddle_coords(coords:list, paddle_x, paddle_y, paddle_width, paddle_height, num_points, colour, delay):

    increment = int(np.ceil((paddle_width*2 + paddle_height*2)/num_points))
    
    if (DELAYS and delay and len(coords) > 3):
        # Turns off colour at the current location
        for _ in range(0, DELAY_LENGTH):
            add_coord(coords, coords[-3], coords[-2], 0)

        # Moves to the Start of the Paddle with the colour still off
        for _ in range(0, DELAY_LENGTH):
            add_coord(coords, paddle_x, paddle_y, 0) 

    # Top Left to Top Right
    for x1 in range(paddle_x, paddle_x+paddle_width, increment):
        add_coord(coords, x1, paddle_y, colour)

    add_coord(coords, paddle_x+paddle_width, paddle_y, colour)

    # Top Right to Bottom Right
    for y1 in range(paddle_y, paddle_y+paddle_height, increment):
        add_coord(coords, paddle_x+paddle_width, y1, colour)

    add_coord(coords, paddle_x+paddle_width, paddle_y+paddle_height, colour)

    # Bottom Right to Bottom Left
    for x2 in range(paddle_x+paddle_width, paddle_x, -increment):
        add_coord(coords, x2, paddle_y+paddle_height, colour)

    add_coord(coords, paddle_x, paddle_y+paddle_height, colour)

    # Bottom Left to Top Left
    for y2 in range(paddle_y+paddle_height, paddle_y, -increment):
        add_coord(coords, paddle_x, y2, colour)

    add_coord(coords, paddle_x, paddle_y, colour)


def add_ball_coords(coords:list, x_center, y_center, radius, num_points, colour):
    # Generate angles evenly spaced around the circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

    if (DELAYS): 
        # Turns off colour at the current location
        for _ in range(0, DELAY_LENGTH):
            add_coord(coords, coords[-3], coords[-2], 0)

        # Moves to the Start of the Paddle with the colour still off
        initial_x = int(x_center + radius * np.cos(angles[0]))
        initial_y = int(y_center + radius * np.sin(angles[0]))
        for _ in range(0, DELAY_LENGTH):
            add_coord(coords, initial_x, initial_y, 0) 
    
    # Calculate the x and y coordinates of the points
    for angle in angles:
        x = int(x_center + radius * np.cos(angle))
        y = int(y_center + radius * np.sin(angle))

        if (x >= 0 and x <= 255 and y >= 0 and y <= 255):
            add_coord(coords, int(x_center + radius * np.cos(angle)), int(y_center + radius * np.sin(angle)), colour)

def add_coord(coords:list, x, y, colour):
    coords.append(x)
    coords.append(y)
    coords.append(colour)

#init serial
serialPort = serial.Serial(
    port="COM4", baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
)

def readSerial():
    successes = 0
    while 1:
    # Read data out of the buffer until a carraige return / new line is found
        #serialString = serialPort.read_until(expected="\n", size=10)

        serialString = serialPort.readline()
        if serialString:
            try:
                print(serialString.decode("ascii"))
            except:
                print(serialString)


readThread = Thread(target = readSerial)
readThread.daemon = True
readThread.start()


DELAY_LENGTH = 2
DELAYS = True
start_pong_game()