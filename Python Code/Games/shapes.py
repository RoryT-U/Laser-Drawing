

def rectangle_points(x:int, y:int, width:int, height:int, corner_len:int, corner_repeats:int, num_non_corner_points:int):
  points = []
  corner_points = (corner_len * 2 - 1) * corner_repeats
  width_without_corners = width - 2 * corner_len + 1
  height_without_corners = height - 2 * corner_len + 1

  width_height_ratio = width_without_corners/height_without_corners

  num_points_on_width = round((num_non_corner_points) * width_height_ratio / 2)
  num_points_on_height = round((num_non_corner_points - num_points_on_width*2) / 2)
  print(corner_points, num_points_on_width, num_points_on_height)

  gap_between_width_points = width_without_corners/num_points_on_width
  gap_between_height_points = height_without_corners/num_points_on_height

  print(gap_between_width_points, gap_between_height_points)

  # Top left Corner
  for i in range(0, corner_len):
    for _ in range(0, corner_repeats):
      points.append([x+i, y])

  
  # Add Top Side 
  for i in range(1, num_points_on_width):
    points.append([x + corner_len - 1 + (i)*gap_between_width_points, y])

  # Top Right Corner
  for i in range(width-corner_len, width):
    for _ in range(0, corner_repeats):
      points.append([x+i,y])
  
  for j in range(1, corner_len):
    for _ in range(0, corner_repeats):
      points.append([x+width-1,y+j])
  
  # Add Right Side
  for j in range(1, num_points_on_height):
    points.append([x+width-1, y+corner_len - 1 + j*gap_between_height_points])

  # Bottom Right Corner
  for j in range(height-corner_len, height):
    for _ in range(0, corner_repeats):
      points.append([x+width-1,y+j])
  
  for i in range(width-2, width-corner_len-1, -1):
    for _ in range(0, corner_repeats):
      points.append([x+i,y+height-1])

  # Add Bottom Side 
  for i in range(num_points_on_width-1, 0, -1):
    points.append([x + corner_len - 1 + (i)*gap_between_width_points, y+height-1])

  # Bottom Left Corner
  for i in range(corner_len-1, -1, -1):
    for _ in range(0, corner_repeats):
      points.append([x+i,y+height-1])

  for j in range(1, corner_len):
    for _ in range(0, corner_repeats):
      points.append([x,y+height-1-j])

  # Add Right Side
  for i in range(1, num_points_on_height):
    points.append([x, y+height - corner_len - i*gap_between_height_points])

  # Close Top Left Corner
  for j in range(corner_len-1, 0, -1):
    for _ in range(0, corner_repeats):
      points.append([x, y+j])

  points.append(points[0])

  print(len(points))
  print(points)
  return points