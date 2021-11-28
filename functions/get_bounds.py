# returns the bounding box of the square basel map as a list
# [x_min, x_max, y_min, y_max]
def get_bounds():
    f = open("maps/basel_square_koords.txt", "r")
    s = f.read()
    f.close()

    box = [float(x) for x in s[:-1].split(",")]
    return box
