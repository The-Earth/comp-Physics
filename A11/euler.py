from matplotlib import pyplot as plt
from scipy import cos, sqrt
dt = 1e-1  # time unit


class HarmonicMass:
    k = 10   # Spring parameter

    def __init__(self, x_0, v_0):
        self.x = x_0
        self.v = v_0
        self.pre_v = v_0

    def acceleration(self):
        return -HarmonicMass.k * self.x

    def update_v(self):
        self.pre_v = self.v
        self.v = self.pre_v + self.acceleration() * dt
        return self.v

    def update_x(self):
        self.x = self.x + (self.pre_v + self.v) / 2 * dt
        return self.x


x_list = []
v_list = []
t_list = []
cur_t = 0
max_t = 10

mp = HarmonicMass(x_0=1, v_0=0)

while cur_t <= max_t:
    x_list.append(mp.x)
    v_list.append(mp.v)
    t_list.append(cur_t)
    mp.update_v()
    mp.update_x()
    cur_t += dt

theory_x = [cos(sqrt(10) * t) for t in t_list]

plt.scatter(t_list, x_list, c='blue', marker='.', s=3)
plt.plot(t_list, theory_x, c='red', lw=1)
plt.savefig('euler.png')
plt.show()
