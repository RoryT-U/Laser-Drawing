
inputFile = "hands-1000.csv";
parts = inputFile.split(".")
f1 = open(inputFile, "r")

# open and read the file after the appending:
f2 = open(parts[0]+"-x."+parts[1], "w")
f3 = open(parts[0]+"-y."+parts[1], "w")

line = f1.readline()
x_list = []
y_list = []
while True:
    line = f1.readline()
    if not line:
        break

    x = line.split(",")
    x_list.append(float(x[0]))
    y_list.append(float(x[1]))

minX = min(x_list)
width = max(x_list) - minX
minY = min(y_list)
height = max(y_list) - minY

scalingFactor = max(width, height)/255

for i in range(0, len(x_list)):
    x_list[i] = (x_list[i] - minX)/scalingFactor
    y_list[i] = (y_list[i] - minY)/scalingFactor


for i in range(0, len(x_list)):
    if x_list[i] > 255.0 or y_list[i] > 255.0:
        print("bad")
    f2.write(str(int(x_list[i])) + ',')
    f3.write(str(int(y_list[i])) + ',')

f1.close()
f2.close()
f3.close()

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

