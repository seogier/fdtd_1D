import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from matplotlib.text import Text

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(-1, 1))

rect = patches.Rectangle((100, -1), 50, 2, color = 'pink')
rect2 = patches.Rectangle((150, -1), 50, 2, color = 'orange')

ax.add_patch(rect)
ax.add_patch(rect2)

ax.text(100, .8, r'Matching Layer', size = 'x-large')
ax.text(150, .6, r'$\varepsilon_r = 9$', size = 'x-large')
plt.title('One-Dimensional Wave with Matching Layer')
plt.xlabel('Space')
plt.ylabel('Amplitude')

line, = ax.plot([], [], lw=1)

class FDTD:
    """1-D Finite Difference Time Domain
    """
    
    def __init__(self):
        self.Z0 = 377.5
        self.dx = 1
        self.N = 200
        self.Ez = np.zeros(self.N)
        self.Hy = np.zeros(self.N)
        self.k = np.ones(self.N)
        self.t = 0
        self.dt = 1
        #Ez is to the left of Hz
    
    def imped(self, index, k):
        self.k[index:] = k
    
    def step(self):
        # Absorbing Boundary Condition
        self.Hy[-1] = self.Hy[-2]
        # Update H Field
        self.Hy[0:-1] += self.dt/self.dx * (self.Ez[1:] - self.Ez[0:-1]) / self.Z0
        
        # Absorbing Boundary Condition
        self.Ez[0] = self.Ez[1]
        # Update E Field
        self.Ez[1:] += self.dt/self.dx * (self.Hy[1:] - self.Hy[0:-1]) * self.Z0 / self.k[1:]
        # Source
        self.Ez[50] -= self.dt * self._gauss(self.t)
        #self.Ez[0] = np.exp(-(self.t-30)*(self.t-30)/100)
        self.t += self.dt

    def _gauss(self, t):
        return np.exp(-(t-30)*(t-30)/100)
    
    def _sine(self, t):
        periods = 3
        l = 70
        if (t<l):
            return np.sin(t* 2 * np.pi* periods/l) * np.exp(-(t-l)*(t-l)/100)
        else:
            return 0

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
start = 1
stop = 9
steps = 50
for i in range(steps):
    d1.imped(100+i, np.exp(i/steps*np.log(stop)))

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    d1.step()
    line.set_data(*d1.state())
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
