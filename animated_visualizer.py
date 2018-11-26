import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def animateTSP(history, points, acc_list, tem_list, weight_list, iteration_time):
    ''' animate the solution over time

        Parameters
        ----------
        hisotry : list
            history of the solutions chosen by the algorith
        points: array_like
            points with the coordinates
    '''

    ''' approx 1500 frames for animation '''
    key_frames_mult = len(history) // 1500

    # fig, ax = plt.subplots()
    fig = plt.figure()
    ax = fig.add_subplot(221)

    ax_acc = fig.add_subplot(222)
    ax_acc.set_title('acceptance probability')

    ax_wgt = fig.add_subplot(223)
    ax_wgt.set_title('weight')

    ax_tem = fig.add_subplot(224)
    ax_tem.set_title('temperature')

    # ax = plt.subplot2grid((2, 2), (0, 0), colspan = 1, rowspan = 1)

    ''' path is a line coming through all the nodes '''
    line, = ax.plot([], [], lw=2)

    def init():
        ''' initialize node dots on graph '''
        x = [points[i][0] for i in history[0]]
        y = [points[i][1] for i in history[0]]
        ax.plot(x, y, 'co')

        # ax_acc.plot(x_iter, acc_list)

        ''' draw axes slighty bigger  '''
        extra_x = (max(x) - min(x)) * 0.05
        extra_y = (max(y) - min(y)) * 0.05
        ax.set_xlim(min(x) - extra_x, max(x) + extra_x)
        ax.set_ylim(min(y) - extra_y, max(y) + extra_y)
        ax.set_title('current solution')

        ax_acc.set_xlim(0, iteration_time)
        ax_acc.set_ylim(0 - 0.05, 1 + 0.05)

        ax_wgt.set_xlim(0, iteration_time)
        ax_wgt.set_ylim(0, max(weight_list))

        ax_tem.set_xlim(0, iteration_time)
        ax_tem.set_ylim(0, max(tem_list))

        line_init = ax_wgt.axhline(y=weight_list[0], color='r', linestyle='--')
        line_min = ax_wgt.axhline(
            y=min(weight_list), color='g', linestyle='--')
        ax_wgt.legend([line_init, line_min], [
                      'Initial weight', 'Optimized weight'])

        '''initialize solution to be empty '''
        line.set_data([], [])
        return line,

    def update(frame):
        ''' for every frame update the solution on the graph '''
        x = [points[i, 0] for i in history[frame] + [history[frame][0]]]
        y = [points[i, 1] for i in history[frame] + [history[frame][0]]]
        line.set_data(x, y)

        x_iter = list(range(iteration_time))
        # print(frame)
        ax_acc.plot(x_iter[frame - 50: frame],
                    acc_list[frame-50: frame], 'bo', markersize=1)

        ax_wgt.plot(x_iter[frame], weight_list[frame], 'bo', markersize=1)

        ax_tem.plot(x_iter[frame], tem_list[frame], 'bo', markersize=1)

        return line

    ''' animate precalulated solutions '''

    ani = FuncAnimation(fig, update, frames=range(0, len(history), key_frames_mult),
                        init_func=init, interval=3, repeat=False)

    plt.show()
