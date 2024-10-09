import keyboard
import pygame
import random
import numpy as np
from pyparsing import col
import serial
import time
from threading import Thread
import random

from PSoCBridge import PSoCBridge
import Utils



LASER_ON_DELAY = 7        # Point delay before turning the laser back on
LASER_OFF_DELAY = 5         # Point delay before turning the laser off
DRAW_WALLS = True

PADDLE_1_COLOUR = PSoCBridge.C_BLUE
PADDLE_2_COLOUR = PSoCBridge.C_GREEN
BALL_WALL_COLOUR = PSoCBridge.C_RED


LASER_ON_DELAY = 10         # Point delay before turning the laser back on
LASER_OFF_DELAY = 5         # Point delay before turning the laser off
DRAW_WALLS = True

class Pong:
    def __init__(self, PSoC):
        self.PSoC = PSoC

    def start_pong_game(self):
        # Initialize pygame
        pygame.init()

        # Set up the screen
        width, height = 255, 255

        # Ball settings
        INITIAL_BALL_VELOCITY_Y = 0.1
        default_ball_speed = 2
        ball_radius = 5
        ball_velocity_x = default_ball_speed * random.choice((1, -1))
        ball_velocity_y = INITIAL_BALL_VELOCITY_Y
        ball_x, ball_y = width // 2, height // 2

        # Paddle settings
        paddle_width, paddle_height = 10, 50
        paddle_velocity = 8
        player_one_x, player_one_y = 5, height // 2 - paddle_height // 2
        player_two_x, player_two_y = width - 5 - paddle_width, height // 2 - paddle_height // 2

        # Scores
        player_score, opponent_score = 0, 0

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Movement keys
            keys = pygame.key.get_pressed()
            if keyboard.is_pressed('s') and player_one_y > 0:
                player_one_y -= paddle_velocity

                if (player_one_y < 0):
                    player_one_y = 0

            if keyboard.is_pressed('w') and player_one_y < height - paddle_height:
                player_one_y += paddle_velocity

                if (player_one_y > height - paddle_height):
                    player_one_y = height - paddle_height

            if keyboard.is_pressed('down') and player_two_y > 0:
                player_two_y -= paddle_velocity

                if (player_two_y < 0):
                    player_two_y = 0

            if keyboard.is_pressed('up') and player_two_y < height - paddle_height:
                player_two_y += paddle_velocity

                if (player_two_y > height - paddle_height):
                    player_two_y = height - paddle_height

            # Ball movement
            ball_x += ball_velocity_x
            ball_y += ball_velocity_y

            # Ball collision with top and bottom walls
            if ball_y - ball_radius < 0:
                ball_velocity_y = -ball_velocity_y
                ball_y = ball_radius

            elif ball_y + ball_radius > height:
                ball_velocity_y = -ball_velocity_y
                ball_y = height - ball_radius

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
                ball_velocity_y = INITIAL_BALL_VELOCITY_Y
            if ball_x > width:
                player_score += 1
                ball_x, ball_y = width // 2, height // 2
                ball_velocity_x = default_ball_speed * random.choice((1, -1))
                ball_velocity_y = INITIAL_BALL_VELOCITY_Y
            
            # Actual coordinates to draw
            to_send = []
            self.add_paddle_coords(to_send, player_one_x, player_one_y, PADDLE_1_COLOUR, self.paddle_1_coords)
            self.add_ball_coords(to_send, ball_x, ball_y, ball_radius, 30, BALL_WALL_COLOUR)
            self.add_paddle_coords(to_send, player_two_x, player_two_y, PADDLE_2_COLOUR, self.paddle_2_coords)

            if DRAW_WALLS:
                # Bottom Wall
                for _ in range(0, LASER_ON_DELAY+1):
                    self.add_coord(to_send, 255, 255, 0)

                for i in range(255, -1, -5):
                    self.add_coord(to_send, i, 255, BALL_WALL_COLOUR)

                for _ in range(0, LASER_OFF_DELAY):
                    self.add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])

                # Top Wall
                for _ in range(0, LASER_ON_DELAY+1):
                    self.add_coord(to_send, 0, 0, 0)

                for i in range(0, 256, 5):
                    self.add_coord(to_send, i, 0, BALL_WALL_COLOUR)

                for _ in range(0, LASER_OFF_DELAY):
                    self.add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])

            print(len(to_send))
            self.PSoC.write(bytearray(list(to_send)))

    
            # Frame rate
            pygame.time.Clock().tick(30)

        # Quit pygame
        pygame.quit()

    # Theses are generated from paddle_offset and then slightly reorder
    paddle_1_coords = [[9, 0], [9, 0], [9, 0], [9, 1], [9, 1], [9, 1], [9, 2], [9, 2], [9, 2], [9, 7], [9, 12], [9, 17], [9, 22], [9, 27], [9, 32], [9, 37], [9, 42], [9, 47], [9, 47], [9, 47], [9, 48], [9, 48], [9, 48], [9, 49], [9, 49], [9, 49], [8, 49], [8, 49], [8, 49], [7, 49], [7, 49], 
    [7, 49], [2, 49], [2, 49], [2, 49], [1, 49], [1, 49], [1, 49], [0, 49], [0, 49], [0, 49], [0, 48], [0, 48], [0, 48], [0, 47], [0, 47], [0, 47], [0, 42], [0, 37], [0, 32], [0, 27], [0, 22], [0, 17], [0, 12], [0, 7],[0, 2], [0, 2], [0, 2], [0, 1], [0, 1], [0, 1], [0, 0], [0, 0], [0, 0], [1, 0], [1, 0], [1, 0], [2, 0], [2, 0], [2, 0], [7, 0], [7, 0], [7, 0], [8, 0], [8, 0], [8, 0], [9, 0]]

    paddle_2_coords = [[0, 0], [0, 0], [0, 0], [1, 0], [1, 0], [1, 0], [2, 0], [2, 0], [2, 0], [7, 0], [7, 0], [7, 0], [8, 0], [8, 0], [8, 0], [9, 0], [9, 0], [9, 0], [9, 1], [9, 1], [9, 1], [9, 2], [9, 2], [9, 2], [9, 7], [9, 12], [9, 17], [9, 22], [9, 27], [9, 32], [9, 37], [9, 42], [9, 47], [9, 47], [9, 47], [9, 48], [9, 48], [9, 48], [9, 49], [9, 49], [9, 49], [8, 49], [8, 49], [8, 49], [7, 49], [7, 49], 
    [7, 49], [2, 49], [2, 49], [2, 49], [1, 49], [1, 49], [1, 49], [0, 49], [0, 49], [0, 49], [0, 48], [0, 48], [0, 48], [0, 47], [0, 47], [0, 47], [0, 42], [0, 37], [0, 32], [0, 27], [0, 22], [0, 17], [0, 12], [0, 7],[0, 2], [0, 2], [0, 2], [0, 1], [0, 1], [0, 1], [0, 0]]

    # Paddles to Coordinates
    def add_paddle_coords(self, coords:list, paddle_x, paddle_y, colour, offsets):

        for _ in range(0, LASER_ON_DELAY):
            self.add_coord(coords, paddle_x + offsets[0][0], paddle_y + offsets[0][1], 0)

        for offset in offsets:
            self.add_coord(coords, paddle_x + offset[0], paddle_y + offset[1], colour)

        for _ in range(0, LASER_OFF_DELAY):
            self.add_coord(coords, coords[-3], coords[-2], coords[-1])

        
    def add_ball_coords(self, coords:list, x_center, y_center, radius, num_points, colour):
        # Generate angles evenly spaced around the circle
        angles = np.linspace(0.1, 2 * np.pi, num_points, endpoint=False)

        first = True
        first_x = 0
        first_y = 0

        for angle in angles:
            # Calculate the x and y coordinates of the points
            x = int(round(x_center + radius * np.cos(angle)))
            y = int(round(y_center + radius * np.sin(angle)))

            if (x >= 0 and x <= 255 and y >= 0 and y <= 255):
                if (first):
                    for _ in range(0, LASER_ON_DELAY+2):
                        self.add_coord(coords, x, y, 0)
                    first_x = x
                    first_y = y
                    first = False
                    
                self.add_coord(coords, x, y, colour)

        for _ in range(0, LASER_OFF_DELAY+4):
            self.add_coord(coords, first_x, first_y, colour)



    def add_coord(self, coords:list, x, y, colour):

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
