from matplotlib import pyplot as plt
from scipy import sin, cos, sqrt, random, pi, exp
import pickle

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.ion()
dt = 0.1
t_max = 80
num_of_atom = 256
T_eq = 0.2
max_x = 10
max_y = 10


class Mass:

    def __init__(self, _x, _y, vx0, vy0, k=1.):
        self.x = _x
        self.prev_x = _x
        self.y = _y
        self.prev_y = _y
        self.vx = vx0
        self.vy = vy0
        self.ax = 0
        self.prev_ax = 0
        self.ay = 0
        self.prev_ay = 0
        self.k = k

    def update_r(self, _max_x, _max_y):
        self.prev_x, self.prev_y = self.x, self.y
        self.x = self.x + self.vx * dt + 0.5 * self.ax * dt ** 2
        self.y = self.y + self.vy * dt + 0.5 * self.ay * dt ** 2

        # # Periodical boundary
        # if self.x > _max_x or self.x < 0:
        #     self.x = self.x - self.x // _max_x * _max_x
        # if self.y > _max_y or self.y < 0:
        #     self.y = self.y - self.y // _max_y * _max_y

        # Hard boundary
        if self.x > _max_x - 0.2 or self.x < 0.2:
            self.vx = -self.vx
        if self.y > _max_y - 0.2 or self.y < 0.2:
            self.vy = -self.vy

        return self.x, self.y

    def update_v(self):
        self.vx = self.vx + 0.5 * (self.prev_ax + self.ax) * dt
        self.vy = self.vy + 0.5 * (self.prev_ay + self.ay) * dt
        return self.vx, self.vy

    def update_a(self, all_atoms, prev: bool):
        ax, ay = 0, 0
        if prev:
            self.prev_ax, self.prev_ay = self.ax, self.ay
            return self.prev_ax, self.prev_ay

        for _atom in all_atoms:
            assert isinstance(_atom, Mass)
            if _atom == self:
                continue
            dx = self.x - _atom.x
            dy = self.y - _atom.y
            dr = sqrt(dx ** 2 + dy ** 2)
            if dr > 1.5:  # Cut-off
                pass
            else:
                ax += self.k * (2 * dr ** (-13) - dr ** (-7)) * dx / dr
                ay += self.k * (2 * dr ** (-13) - dr ** (-7)) * dy / dr

        self.ax = ax
        self.ay = ay
        return ax, ay


def get_system_temperature(all_atoms, dimension, amount):
    _sum = 0
    for _atom in all_atoms:
        assert isinstance(_atom, Mass)
        _sum += 0.5 * (_atom.vx ** 2 + _atom.vy ** 2)
    return 2 * _sum / dimension / amount


def temperature_adjust(_T_cur):
    for _atom in atom_list:
        _atom.vx = _atom.vx * ((T_eq / _T_cur) ** 0.5)
        _atom.vy = _atom.vy * ((T_eq / _T_cur) ** 0.5)


def move():
    plt.cla()
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    for _atom in atom_list:
        _atom.update_a(atom_list, prev=True)
        _atom.update_a(atom_list, prev=False)
    for _atom in atom_list:
        _atom.update_v()
    for _atom in atom_list:
        _atom.update_r(max_x, max_y)
        plt.scatter(_atom.x, _atom.y, c='blue', s=6)

    plt.pause(0.1e-2)


def maxwell_dist():
    while True:
        _x = random.uniform(-3, 3)
        _y = random.uniform(0, 1)
        if _y < _x ** 2 * exp(-_x ** 2):
            return _x


if __name__ == '__main__':
    cur_t = 0
    atom_list, T_list = [], []
    t_list = []
    # Initialization
    for i in range(num_of_atom):
        x0, y0 = 0.55 * (i % 16) + random.uniform(0.9, 1.1), 0.55 * (i // 16) + random.uniform(0.9, 1.1)
        v0, theta0 = 0.1 * maxwell_dist(), random.uniform(0, 2 * pi)
        atom_list.append(Mass(x0, y0, v0 * cos(theta0), v0 * sin(theta0), k=1e-7))
        # plt.plot(x0, y0, c='blue')

    while cur_t < t_max:
        move()
        T_cur = get_system_temperature(atom_list, 2, num_of_atom)
        if abs(T_cur - T_eq) > 1:
            temperature_adjust(T_cur)
        T_list.append(T_cur)
        t_list.append(cur_t)
        print(cur_t / t_max)
        cur_t += dt

    plt.ioff()
    plt.cla()
    plt.autoscale()
    plt.xlabel('t')
    plt.ylabel('Ek')
    plt.plot(t_list, T_list, c='blue')
    plt.savefig('1.png')
    plt.show()

    v_list = []
    vx_list = []
    vy_list = []

    for atom in atom_list:
        v_list.append((atom.vx ** 2 + atom.vy ** 2) ** 0.5)
        vx_list.append(atom.vx)
        vy_list.append(atom.vy)

    plt.cla()
    plt.hist(v_list, bins=16)
    plt.xlabel('v')
    plt.ylabel('numbers')
    plt.savefig('V.png')
    plt.show()

    plt.cla()
    plt.hist(vx_list, bins=16)
    plt.xlabel('vx')
    plt.ylabel('numbers')
    plt.savefig('Vx.png')
    plt.show()

    plt.cla()
    plt.hist(vy_list, bins=16)
    plt.xlabel('vy')
    plt.ylabel('numbers')
    plt.savefig('Vy.png')
    plt.show()

    pickle.dump(atom_list, open('atom_list.pkl', 'wb'))
