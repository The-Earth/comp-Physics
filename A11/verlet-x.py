from matplotlib import pyplot as plt
dt = 1e-2   # time unit


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
        self.pre_x = cur_x
        return self.x


cur_t = 0
max_t = 10
x_list = []

mp = HarmonicMass(x_0=1, v_0=0)

while cur_t <= max_t:
    plt.scatter(cur_t, mp.x, c='blue', marker='.')
    x_list.append(mp.x)
    mp.update_x()
    cur_t += dt

plt.savefig('verlet-x_x-t.png')
print(x_list)
plt.show()
