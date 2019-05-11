from matplotlib import pyplot as plt
from scipy import cos, sqrt
dt = 1e-2  # time unit


class HarmonicMass:
    k = 10

    def __init__(self, x_0, v_0):
        self.x = x_0
        self.pre_x = x_0
        self.v = v_0

    def acceleration(self):
        return -HarmonicMass.k * self.x

    def update_x(self):
        cur_x = self.x
        self.x = 2 * cur_x - self.pre_x + self.acceleration() * dt**2
        self.v = (self.pre_x - self.x) / (2 * dt)
        self.pre_x = cur_x
        return self.x


cur_t = 0
max_t = 2
x_list = []
v_list = []
t_list = []

mp = HarmonicMass(x_0=1, v_0=0)

while cur_t <= max_t:
    v_list.append(mp.v)
    x_list.append(mp.x)
    t_list.append(cur_t)
    mp.update_x()
    cur_t += dt

theory_x = [cos(sqrt(10) * t) for t in t_list]

plt.scatter(t_list, x_list, c='blue', marker='.', s=3)
plt.plot(t_list, theory_x, c='red', lw=1)
plt.savefig('phase_verlet-x.png')
plt.show()
