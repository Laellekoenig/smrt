import matplotlib.pyplot as plt

def get_basel_square(bw=False):
    if bw:
        return plt.imread("maps/basel_square_bw.jpg")
    else:
        return plt.imread("maps/basel_square.png")
