import numpy as np

def generate_axes():
    """
    Generates x and y axis values based on a sine function.

    The function populates two lists, xAxis and yAxis, with values calculated
    using the sine function. The calculations are based on the index and a
    scaling factor.

    Returns:
        tuple: A tuple containing two lists (xAxis, yAxis).
    """
    # Initialize the lists to hold the axis values
    xAxis = [0] * 2040  # Preallocate list for x-axis values
    yAxis = [0] * 2040  # Preallocate list for y-axis values

    # Populate the xAxis and yAxis lists
    for i in range(0, 2040, 1):
        xAxis[i] = int(2040 * np.sin(np.pi * (2*i + 1020) / 2040) + 2040)
        yAxis[i] = int(2040 * np.sin(np.pi * 2*i / 2040) + 2040)

    return xAxis, yAxis

# Example usage
xAxis, yAxis = generate_axes()


x = []
y = []

for i in range(0, len(xAxis), 4):
    x.append(xAxis[i])

for i in range(0, len(yAxis), 4):
    y.append(yAxis[i])

print(x)
print(y)