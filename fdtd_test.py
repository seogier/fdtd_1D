from fdtd import FDTD

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.text import Text

fig = plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(-1, 1))

plt.title('One-Dimensional Wave with Absorbing BC')
plt.xlabel('Space')
plt.ylabel('Amplitude')

line, = ax.plot([], [], lw=1)

d1 = FDTD()
d1.ABC = False

def init():
    line.set_data([[], []])
    return line,

def animate(i):
    d1.step()
    line.set_data(*d1.state())
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)
plt.show()