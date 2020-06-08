#from matplotlib import animation
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib import animation

class FDTD:
    """1-D Finite Difference Time Domain
    """
    
    def __init__(self):
        self.Z0 = 377.5
        self.dx = .5
        self.N = 200
        self.Ez = np.zeros(self.N)
        self.Hy = np.zeros(self.N)
        self.t = 0
        self.dt = 1
        #Ez is to the left of Hz
    
    def step(self):
        self.Hy[0:-1] = self.Hy[0:-1] + (self.Ez[1:] - self.Ez[0:-1]) / self.Z0
        self.Ez[1:] = self.Ez[1:] + (self.Hy[1:] - self.Hy[0:-1]) * self.Z0
        # Source
        self.Ez[0] = np.exp(-(self.t-30)*(self.t-30)/100)
        self.t += self.dt

    def steps(self, i):
        st = 0
        while st<i:
            self.step()
            st +=1

    def state(self):
        x = np.linspace(0,self.N-1,self.N)
        y = self.Ez
        return (x,y)

d1 = FDTD()
d1.step()
fig = plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(0, 1))
line, = ax.plot([], [], lw = 2)

def init():
    line.set_data([[],[]])
    return line

def animate(i):
    global d1
    d1.step()
    line.set_data(*d1.state())
    return line

anim = animation.FuncAnimation(fig, animate, init_func=init, frames = 1, interval=200, blit=True)
#t = np.arange(0.0, 2.0, 0.01)
#s = np.sin(2*np.pi*t)
#plt.plot(t, s, linewidth=1.0)
#plt.plot(*d1.state())
plt.show()