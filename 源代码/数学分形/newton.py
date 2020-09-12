# Python绘制牛顿分形
# 公众号：Charles的皮卡丘
import numpy as np
import matplotlib.pyplot as plt
# from numba import jit


# 函数
# @jit('complex64(complex64)', nopython=True)
def f(z):
    # slow
    # return z**3 - 1
    # quicker
    return z*z*z - 1


# 导数
# @jit('complex64(complex64)', nopython=True)
def df(z):
    return 3*z*z


# 迭代器
# @jit('float64(complex64)', nopython=True)
def iterate(z):
    num = 0
    while abs(f(z)) > 1e-4:
        w = z - f(z)/df(z)
        num += np.exp(-1/abs(w-z))
        z = w
    return num


# 画牛顿环
def draw(imgsize=600):
    y, x = np.ogrid[1: -1: imgsize*2j, -1: 1: imgsize*2j]
    z = x + y*1j
    img = np.frompyfunc(iterate, 1, 1)(z).astype(np.float)
    fig = plt.figure(figsize=(imgsize/100.0, imgsize/100.0), dpi=100)
    axi = fig.add_axes([0, 0, 1, 1], aspect=1)
    axi.axis('off')
    axi.imshow(img, cmap='hot')
    fig.savefig('newton.png')
    

if __name__ == '__main__':
    draw()