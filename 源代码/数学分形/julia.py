# Python绘制朱利亚分形
# 公众号：Charles的皮卡丘
import numpy as np
import matplotlib.pyplot as plt
from numba import jit


MaxIters = 500
Radius = 4
Const = 0.7


@jit('float32(complex64)')
def escape(z):
    for i in range(MaxIters):
        if z.real * z.real + z.imag * z.imag > Radius:
            break
        z = (z*z + Const) / (z*z - Const)
    return i


def draw(xmin=-2, xmax=2, ymin=-1.6, ymax=1.6, width=800, height=640):
    y, x = np.ogrid[ymax: ymin: height*2j, xmin: xmax: width*2j]
    z = x + y*1j
    img = np.asarray(np.frompyfunc(escape, 1, 1)(z)).astype(np.float)
    img /= np.max(img)
    img = np.sin(img**2 * np.pi)
    fig = plt.figure(figsize=(width/100.0, height/100.0), dpi=100)
    axi = fig.add_axes([0, 0, 1, 1], aspect=1)
    axi.axis('off')
    axi.imshow(img, cmap='hot')
    fig.savefig('julia.png')


if __name__ == '__main__':
    draw()