import numpy as np

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
        self.ABC = True
        #Ez is to the left of Hz

    def imped(self, index, k):
        self.k[index:] = k
   
    def step(self):
        # Enfofce Absorbing Boundary Condition if specified
        if self.ABC:
            self.Hy[-1] = self.Hy[-2]
        else:
            self.Hy[-1] = 0
        # Update H Field
        self.Hy[0:-1] += self.dt/self.dx * (self.Ez[1:] - self.Ez[0:-1]) / self.Z0
        
        # Enfofce Absorbing Boundary Condition if specified
        if self.ABC:
            self.Ez[0] = self.Ez[1]
        else:
            self.Ez[0] = 0

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
