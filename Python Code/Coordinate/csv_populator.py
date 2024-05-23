
def coordinate_converter(input_file):
    f1 = open("raw_csv/"+inputFile, "r")

    parts = input_file.split(".")

    f2 = open("converted_csvs/"+parts[0]+"-x."+parts[1], "w")
    f3 = open("converted_csvs/"+parts[0]+"-y."+parts[1], "w")

    line = f1.readline()  # ignore first line
    x_list = []
    y_list = []
    while True:  # read all the values from the csv
        line = f1.readline()
        if not line:
            break

        x = line.split(",")
        x_list.append(float(x[0]))
        y_list.append(float(x[1]))

    # determine in minimal values and scaling_factor
    min_x = min(x_list)
    width = max(x_list) - min_x
    min_y = min(y_list)
    height = max(y_list) - min_y

    scaling_factor = max(width, height)/255

    # translate all coordinates by min_x and
    # min_y then apply scaling_factor
    for i in range(0, len(x_list)):
        scaled_x_coord = (x_list[i] - min_x)/scaling_factor
        scaled_y_coord = (y_list[i] - min_y)/scaling_factor

        # check coordinates are valid
        if (scaled_x_coord > 255.0 or scaled_x_coord < 0
                or scaled_y_coord > 255.0 or scaled_y_coord < 0):
            print("Invalid scaled coordinate")

        f2.write(str(int(scaled_x_coord)) + ',')
        f3.write(str(int(scaled_y_coord)) + ',')

    f1.close()
    f2.close()
    f3.close()


def square_coordinate():
    f1 = open("converted_csvs/square_coords_100_x.csv", "w")
    f2 = open("converted_csvs/square_coords_100_y.csv", "w")

    sizes = 250
    for x in range(0, sizes * 4, 10):

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

        f1.write('\n,')
        f2.write(',')


def snake():
    f1 = open("converted_csvs/snaked-lines-x.csv", "w")
    f2 = open("converted_csvs/snaked-lines-y.csv", "w")

    sizes = 250
    f1.write("0")
    f2.write("0")
    for x in range(0, 9, 2):
        f1.write(",255,255,0,0")
        y = x*25
        f2.write(','+str(y)+","+str(y+25) + ',' + str(y+25) + ',' + str(y+50))


snake()
square_coordinate()

inputFile = "atom-1000.csv"
coordinate_converter(inputFile)

