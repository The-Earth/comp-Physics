from matplotlib import pyplot as plt
from scipy import cos, sqrt
dt = 1e-2   # time unit


class HarmonicMass:

    def __init__(self, x_0, v_0, k):
        self.x = x_0
        self.prev_x = x_0
        self.v = v_0
        self.k = k

    def acceleration(self, cord):
        return -self.k * cord

    def update_x(self):
        self.prev_x = self.x
        self.x = self.x + self.v * dt + 0.5 * self.acceleration(self.prev_x) * dt**2
        return self.x

    def update_v(self):
        self.v = self.v + 0.5 * (self.acceleration(self.prev_x) + self.acceleration(self.x)) * dt
        return self.v


cur_t = 0
max_t = 10
x_list = []
t_list = []
v_list = []

mp = HarmonicMass(x_0=1, v_0=0, k=10)

while cur_t <= max_t:
    x_list.append(mp.x)
    v_list.append(mp.v)
    t_list.append(cur_t)
    mp.update_x()
    mp.update_v()
    cur_t += dt

theory_x = [cos(sqrt(10) * t) for t in t_list]

plt.scatter(t_list, x_list, c='blue', marker='.', s=3)
plt.plot(t_list, theory_x, c='red', lw=1)
plt.savefig('verlet-v.png')
plt.show()
