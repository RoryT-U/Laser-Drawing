
import numpy as np



def paddle_offset_generation(paddle_width, paddle_height, corner_length, side_increments, corner_repeats):
  offsets = []

  y_points = int(((paddle_height - 1)- (corner_length - 1 + side_increments)*2) / side_increments)

  x_points = int(((paddle_width - 1) - (corner_length - 1 + side_increments)*2) / side_increments)

  # Top left corner
  for y in range(corner_length-1, 0, -1):
    for _ in range(0, corner_repeats):
      offsets.append([0,y])

  for x in range(0, corner_length):
    for _ in range(0, corner_repeats):
      offsets.append([x,0])
  
  # Add Top Side 
  # for x in range(0, x_points):
  #   offsets.append([corner_length - 1 + x*side_increments, 0])
  
  # Top Right corner
  for x in range(paddle_width-corner_length, paddle_width):
    for _ in range(0, corner_repeats):
      offsets.append([x,0])
  
  for y in range(1, corner_length):
    for _ in range(0, corner_repeats):
      offsets.append([paddle_width-1,y])

  # Add Right Side
  for y in range(1, y_points+2):
    offsets.append([paddle_width-1, corner_length - 1 + y*side_increments])

  # Bottom Right corner
  for y in range(paddle_height-corner_length, paddle_height):
    for _ in range(0, corner_repeats):
      offsets.append([paddle_width-1,y])
  
  for x in range(paddle_width-2, paddle_width-corner_length-1, -1):
    for _ in range(0, corner_repeats):
      offsets.append([x,paddle_height-1])

  # THIS ONE IS NOT CORRECT, COULDNT BE BOTHERED
  # Add Bottom Side 
  # for x in range(x_points, 0, -1):
  #   offsets.append([corner_length - 1 + x*side_increments, 0])

  # Bottom Left corner
  for x in range(corner_length-1, -1, -1):
    for _ in range(0, corner_repeats):
      offsets.append([x,paddle_height-1])

  for y in range(1, corner_length):
    for _ in range(0, corner_repeats):
      offsets.append([0,paddle_height-1-y])

  # Add Right Side
  for y in range(1, y_points+2):
    offsets.append([0, paddle_height - corner_length - y*side_increments])

  print(offsets)





paddle_offset_generation(10, 50, 3, 2.5, 3)