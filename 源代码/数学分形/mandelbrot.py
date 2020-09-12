# Python绘制曼德勃罗集
# 公众号：Charles的皮卡丘
import numpy as np
from PIL import Image
from numba import jit


MaxIters = 200
Radius = 100


@jit
def color(z, i):
    v = np.log2(i + 1 - np.log2(np.log2(abs(z)))) / 5
    if v < 1.0:
        return v**4, v**2.5, v
    else:
        v = max(0, 2-v)
        return v, v**1.5, v**3


@jit
def iterate(c):
    z = 0j
    for i in range(MaxIters):
        if z.real*z.real + z.imag*z.imag > Radius:
            return color(z, i)
        z = z*z + c
    return 0, 0 ,0


def draw(xmin=-2.1, xmax=0.8, ymin=-1.16, ymax=1.16, width=800, height=640):
    y, x = np.ogrid[ymax: ymin: height*1j, xmin: xmax: width*1j]
    z = x + y*1j
    red, green, blue = np.asarray(np.frompyfunc(iterate, 1, 3)(z)).astype(np.float)
    img = np.dstack((red, green, blue))
    Image.fromarray(np.uint8(img*255)).save('mandelbrot.png')


if __name__ == '__main__':
    draw()