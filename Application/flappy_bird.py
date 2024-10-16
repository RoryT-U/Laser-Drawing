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

from Utils import Shapes;

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

WALL_COLOUR = PSoCBridge.C_ALL
BIRD_COLOUR = PSoCBridge.C_RED
PIPE_COLOUR = PSoCBridge.C_GREEN

LASER_ON_DELAY = 15         # Point delay before turning the laser back on
LASER_OFF_DELAY = 5        # Point delay before turning the laser off
DRAW_WALLS = True

class FlappyBird():
    
    def __init__(self, PSoC):
        self.PSoC = PSoC
        self.running = True

    def stop(self):
        self.running = False
    
    def start_flappy_bird(self):
        # Initialize pygame
        pygame.init()

        # Set up display
        width, height = 255, 255

        # Set up clock
        clock = pygame.time.Clock()
        tick_rate = 15

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

        # Function to create new pipes
        def create_pipe():
            pipe_height = random.randint(20, height - pipe_gap - 20)
            top_pipe = pygame.Rect(width, 0, pipe_width, pipe_height)
            bottom_pipe = pygame.Rect(width, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap)
            return top_pipe, bottom_pipe

        # Main game loop
        game_over = False

        # Create initial pipes
        pipe_list.append(create_pipe())

        while self.running:


            if keyboard.is_pressed('space') and not game_over:
                bird_speed_y = jump_strength
            if keyboard.is_pressed('space') and game_over:
                pipe_list = []
                pipe_spawn_rate = tick_rate * 3  
                pipe_tick = 0
                bird_y = height // 2
                game_over = False
                score = 0
                pipe_list.append(create_pipe())

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
            self.add_bird_coords(to_send, bird_x, bird_y, bird_radius, 50, BIRD_COLOUR)
            
            for pipe in pipe_list:
                self.add_pipe_coords(to_send, pipe[0], PIPE_COLOUR)
                self.add_pipe_coords(to_send, pipe[1], PIPE_COLOUR)


            if DRAW_WALLS:
                # Bottom Wall
                for _ in range(0, LASER_ON_DELAY):
                    self.add_coord(to_send, 255, 255, 0)

                for i in range(255, -1, -5):
                    self.add_coord(to_send, i, 255, WALL_COLOUR)

                for _ in range(0, LASER_OFF_DELAY):
                    self.add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])
                
                self.add_coord(to_send, to_send[-3], to_send[-2], 0)

                # Top Wall
                for _ in range(0, LASER_ON_DELAY):
                    self.add_coord(to_send, 0, 0, 0)

                for i in range(0, 256, 5):
                    self.add_coord(to_send, i, 0, WALL_COLOUR)

                for _ in range(0, LASER_OFF_DELAY):
                    self.add_coord(to_send, to_send[-3], to_send[-2], to_send[-1])
                
                self.add_coord(to_send, to_send[-3], to_send[-2], 0)

            print(len(to_send))
            self.PSoC.write(bytearray(list(to_send)))

            # Frame rate
            clock.tick(tick_rate)

    def add_pipe_coords(self, coords:list[int], pipe:pygame.Rect, colour):
        x_left, y_top = pipe.topleft

        points = Utils.Shapes.rectangle_points(x_left, y_top, pipe.width, pipe.height, 3, 3, 40)

        for _ in range(0, LASER_ON_DELAY):
            self.add_coord(coords, points[0][0], points[0][1], 0)

        for point in points:
            self.add_coord(coords, point[0], point[1], colour)
        
        for _ in range(0, LASER_OFF_DELAY):
            self.add_coord(coords, points[-1][0], points[-1][1], colour)
        

    def add_bird_coords(self, coords:list, x_center, y_center, radius, num_points, colour):
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
                        self.add_coord(coords, x, y, 0)
                    first_x = x
                    first_y = y
                    first = False
                    
                self.add_coord(coords, x, y, colour)

        for _ in range(0, LASER_OFF_DELAY):
            self.add_coord(coords, first_x, first_y, colour)

    @staticmethod
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
        
        coords.append(int(255-x))
        coords.append(int(255-y))   
        coords.append(colour)

