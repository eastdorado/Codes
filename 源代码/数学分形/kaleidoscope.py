# Python绘制二十面体对称的万花筒
# 公众号：Charles的皮卡丘
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb


def Klein(z):
    return 1728 * (z * (z**10 + 11 * z**5 - 1))**5 / \
        (-(z**20 + 1) + 228 * (z**15 - z**5) - 494 * z**10)**3


def RiemannSphere(z):
    t = 1 + z.real*z.real + z.imag*z.imag
    return 2*z.real/t, 2*z.imag/t, 2/t-1


def Mobius(z):
    return (z - 20)/(3*z + 1j)


def draw(imgsize=500):
    y, x = np.ogrid[6: -6: imgsize*2j, -6: 6: imgsize*2j]
    z = x + y*1j
    z = RiemannSphere(Klein(Mobius(Klein(z))))
    H = np.sin(z[0]*np.pi)**2
    S = np.cos(z[1]*np.pi)**2
    V = abs(np.sin(z[2]*np.pi) * np.cos(z[2]*np.pi))**0.2
    HSV = np.dstack((H, S, V))
    img = hsv_to_rgb(HSV)
    fig = plt.figure(figsize=(imgsize/100.0, imgsize/100.0), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], aspect=1)
    ax.axis('off')
    ax.imshow(img)
    fig.savefig('kaleidoscope.png')


if __name__ == '__main__':
    draw()