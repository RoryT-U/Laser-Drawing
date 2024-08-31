import pygame
import random
import numpy as np

def start_pong_game():
    # Initialize pygame
    pygame.init()

    # Set up the screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong Game")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Ball settings
    default_ball_speed = 4
    ball_radius = 15
    ball_velocity_x = default_ball_speed * random.choice((1, -1))
    ball_velocity_y = 0.1
    ball_x, ball_y = width // 2, height // 2

    # Paddle settings
    paddle_width, paddle_height = 20, 100
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
        if keys[pygame.K_s] and player_one_y < height - paddle_height:
            player_one_y += paddle_velocity

        if keys[pygame.K_UP] and player_two_y > 0:
            player_two_y -= paddle_velocity
        if keys[pygame.K_DOWN] and player_two_y < height - paddle_height:
            player_two_y += paddle_velocity


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
        player_one_x_coordinates, player_one_y_coordinates = generate_paddle_coordinates(player_one_x, player_one_y, paddle_width, paddle_height, 200)

        player_two_x_coordinates, player_two_y_coordinates = generate_paddle_coordinates(player_two_x, player_two_y, paddle_width, paddle_height, 200)

        ball_coordinates = generate_ball_coordinates(ball_x, ball_y, ball_radius, 100)

        # TODO NEED TO SEND THE COORDINATES TO PSoC


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
        pygame.time.Clock().tick(60)

    # Quit pygame
    pygame.quit()

# Paddles to Coordinates
def generate_paddle_coordinates(paddle_x, paddle_y, paddle_width, paddle_height, num_points):

    increment = (paddle_width*2 + paddle_height*2)/num_points
    
    x_coordinates = []
    y_coordinates = []
    
    # Top Left to Top Right
    for x1 in range(paddle_x, paddle_x+paddle_width, increment):
        x_coordinates.append(x1)
        y_coordinates.append(paddle_y)

    x_coordinates.append(paddle_x+paddle_width)
    y_coordinates.append(paddle_y)

    # Top Right to Bottom Right
    for y1 in range(paddle_y, paddle_y+paddle_height, increment):
        x_coordinates.append(paddle_x+paddle_width)
        y_coordinates.append(y1)

    x_coordinates.append(paddle_x+paddle_width)
    y_coordinates.append(paddle_y+paddle_height)

    # Bottom Right to Bottom Left
    for x2 in range(paddle_x+paddle_width, paddle_x, -increment):
        x_coordinates.append(x2)
        y_coordinates.append(paddle_y+paddle_height)

    x_coordinates.append(paddle_x)
    y_coordinates.append(paddle_y+paddle_height)

    # Bottom Left to Top Left
    for y2 in range(paddle_y+paddle_height, paddle_y, -increment):
        x_coordinates.append(paddle_x)
        y_coordinates.append(y2)

    x_coordinates.append(paddle_x)
    y_coordinates.append(paddle_y)

    return x_coordinates, y_coordinates


def generate_ball_coordinates(x_center, y_center, radius, num_points):
    # Generate angles evenly spaced around the circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    
    # Calculate the x and y coordinates of the points
    x_coordinates = x_center + radius * np.cos(angles)
    y_coordinates = y_center + radius * np.sin(angles)

    return x_coordinates, y_coordinates

start_pong_game()