import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(-np.pi, np.pi, 100)
# y = np.sin(x)
# plt.plot(x, y)
# plt.show()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(datingDataMat [:, 1], datingDataMat [ :, 2],
# 15.0*array(datingLabels}, 15.0*array(datingLabels))
# plt. show ()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation

# 振幅、波长、角速度
A = 0.5
lm = 1
global w
w = 1
# 暂停标志位,last_time用于存储上一个时间
pause = False
last_time = 0

# 创建两个实例，fig用于返回图像,ax用于绘制动画,可能理解有出入
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
# 创建fig返回的初始图像
x = np.arange(0, 2 * np.pi, 0.01)
line, = ax.plot(x, 2 * A * np.cos(2 * np.pi * x / lm) * np.cos(w * 0))
line2, = ax.plot(x, A * np.cos(w * 0 - 2 * np.pi * x / lm))
line3, = ax.plot(x, A * np.cos(w * 0 + 2 * np.pi * x / lm))


def zhubo(i):
    if pause:
        global last_time
        i = last_time
        return line, line2, line3
    line.set_ydata(2 * A * np.cos(2 * np.pi * x / lm) * np.cos(w * i))
    line2.set_ydata(A * np.cos(w * i - 2 * np.pi * x / lm))
    line2.set_color('g')
    line3.set_ydata(A * np.cos(w * i + 2 * np.pi * x / lm))
    line3.set_color('r')
    last_time = i
    w_text = ax.text(0.05, 0.9, 'Stop', transform=ax.transAxes)
    w_text.set_text('w = ' + str(w))
    return line, line2, line3, w_text


# init一下清理屏幕
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    line2.set_ydata(np.ma.array(x, mask=True))
    line3.set_ydata(np.ma.array(x, mask=True))
    return line,


class Index(object):
    ind = 0

    # 暂停
    def stop(self, event):
        global pause
        pause ^= True

    # 减小w
    def redu(self, event):
        global w
        w -= 1

    # 增加w
    def incr(self, event):
        global w
        w += 1


callback = Index()
# 参数：每一帧返回的图像实例，绘制每一帧的函数，动画长度，
#       是否启用一个函数来刷新，如果不设置则用第二个参数的第一帧刷新
#       帧率？貌似是
#       是否刷新所有的点
zb = animation.FuncAnimation(fig, zhubo, np.arange(1, 10, 0.1), init_func=init,
                             interval=50, blit=True)

# 设置三个功能按钮，并绑定槽函数
axincr = plt.axes([0.39, 0.05, 0.2, 0.075])
axredu = plt.axes([0.6, 0.05, 0.2, 0.075])
axstop = plt.axes([0.81, 0.05, 0.1, 0.075])

bstop = Button(axstop, 'Stop')
bstop.on_clicked(callback.stop)

bredu = Button(axredu, 'Reduce the cycle')
bredu.on_clicked(callback.redu)

bincr = Button(axincr, 'Increase the cycle')
bincr.on_clicked(callback.incr)
# zb.save('111.html')
plt.show()