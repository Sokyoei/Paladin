import numpy as np
from loguru import logger
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes


def main():
    fig = plt.figure()
    ax: Axes = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("frame")
    ax.set_ylabel("value")
    x = np.arange(0, 2 * np.pi, 0.01)  # 生成X轴坐标序列
    (line1,) = ax.plot(x, np.sin(x))  # 获取折线图对象，逗号不可少，如果没有逗号，得到的是元组

    def update(n):
        line1.set_ydata(np.sin(x + n / 10.0))

    ani = FuncAnimation(fig, update, interval=50, blit=False, repeat=False)
    logger.debug(ani)
    plt.show()


if __name__ == "__main__":
    main()
