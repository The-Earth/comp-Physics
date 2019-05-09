from matplotlib import pyplot as plt
dt = 1e-1   # time unit


class harmonicMass:
    k = 10   # Spring parameter

    def __init__(self, x_0, v_0):
        self.x = x_0
        self.v = v_0
        self.pre_v = v_0

    def acceleration(self):
        return -harmonicMass.k * self.x

    def update_v(self):
        self.pre_v = self.v
        self.v = self.pre_v + self.acceleration() * dt
        return self.v

    def update_x(self):
        self.x = self.x + (self.pre_v + self.v) / 2 * dt
        return self.x


x_list = []
v_list = []
cur_t = 0
max_t = 10

mp = harmonicMass(x_0=1, v_0=0)

while cur_t <= max_t:
    # x_list.append(mp.x)
    # v_list.append(mp.v)
    plt.scatter(cur_t, mp.x, c='blue', marker='.')
    mp.update_v()
    mp.update_x()
    cur_t += dt

plt.savefig('x-t.png')
plt.show()
