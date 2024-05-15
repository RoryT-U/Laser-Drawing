f1 = open("coordinator.csv", "r")

# open and read the file after the appending:
f2 = open("converted_coords_x.csv", "w")
f3 = open("converted_coords_y.csv", "w")
f4 = open("converted_coords_decs_x.csv", "w")
f5 = open("converted_coords_decs_y.csv", "w")

line = f1.readline()
while True:
    line = f1.readline()
    if not line:
        break

    x = line.split(",")
    f2.write(x[0].split(".")[0] + ",")
    f3.write(x[1].split(".")[0] + ",")

    f4.write(str(round(float(x[0]), 2)) + ",")
    f5.write(str(round(float(x[1]), 2)) + ",")

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()

f1 = open("square_coords_X.csv", "w")
f2 = open("square_coords_y.csv", "w")

sizes = 255
for x in range(0, sizes * 4):

    if x < sizes:
        f1.write(str(sizes))
        f2.write(str(sizes - x))
    elif x < sizes * 2:
        f1.write(str(sizes - x % sizes))
        f2.write(str(0))
    elif x < sizes * 3:
        f1.write(str(0))
        f2.write(str(x % sizes))
    else:
        f1.write(str(x % sizes))
        f2.write(str(sizes))

    f1.write(',')
    f2.write(',')

