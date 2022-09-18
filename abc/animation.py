"""
=======
animation
=======

Constructing a simple GUI to demonstrate the animation function from the matplotlib module.

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
plt.plot(theta, r)
l, = plt.plot(theta, r)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)

def update(i):
    rr = np.arange(0, 2, 0.01)
    sec = int(np.mod(time.time(), 60))
    rho = 2 * np.pi * (rr - sec/60)
    l.set_xdata(rho)
    plt.draw()


tproc = 200   #time duration in ms of image processing, empirically adjusted
ani = animation.FuncAnimation(fig, update, fargs=(), interval=tproc)
plt.show()
