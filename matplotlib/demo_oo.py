#! /user/bin/python
# _*_ coding: utf-8 _*_

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy
from math import pi

fig = Figure()

# 连接绘图的‘后端’
canvas = FigureCanvas(fig)

# 添加绘图区域（坐标系），两种方式/add_subplot(1, 1, 1)
ax = fig.add_axes([0.1, 0.1, 0.3, 0.3])

line, = ax.plot([0, 1], [0, 1])

ax.set_title('ax')

ax.set_xlabel('xlabel - x value')
ax.set_ylabel('ylabel - y value')
ax.legend()
ax.grid()

ax1 = fig.add_axes([0.1, 0.6, 0.3, 0.3])
ax1.set_title('ax1')
line1, = ax1.plot([0, 1], [0, 1])

# 用函数方法画正余弦函数图形
ax2 = fig.add_axes([0.6, 0.1, 0.3, 0.3])
ax2.set_title('ax2')
x = numpy.linspace(-2*pi, 2*pi, 100)
y = numpy.sin(x)
z = numpy.cos(x)
line2, = ax2.plot(x, y)
line21, = ax2.plot(x, z)

# 用path路径方法画不规则图形
ax3 = fig.add_axes([0.6, 0.6, 0.3, 0.3])
ax3.set_title('ax3')
points = [(0.0, 0.0), (0.0, 1.0), (0.5, 1.5), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]
paints = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY, ]
path = Path(points, paints)
patch = patches.PathPatch(path, facecolor='b')
ax3.set_xlim(-0.5, 2)
ax3.set_ylim(-0.5, 2)
ax3.add_patch(patch)
ax3.grid()

canvas.print_figure('demo.jpg')
