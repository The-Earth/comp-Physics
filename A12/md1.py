from matplotlib import pyplot as plt
from numpy.random import random
from scipy import sin, cos, pi

plt.ion()
dt = 1e-2
cur_t = 0
t_max = 10
num_of_atom = 25
T_eq = 1
max_x = 10
max_y = 10


class Mass:

    def __init__(self, x0, y0, vx0, vy0, k=1.):
        self.x = x0
        self.prev_x = x0
        self.y = y0
        self.prev_y = y0
        self.vx = vx0
        self.vy = vy0
        self.ax = 0
        self.prev_ax = 0
        self.ay = 0
        self.prev_ay = 0
        self.k = k

    def update_r(self, max_x, max_y):
        self.prev_x, self.prev_y = self.x, self.y
        self.x = self.x + self.vx * dt + 0.5 * self.ax * dt**2
        self.y = self.y + self.vy * dt + 0.5 * self.ay * dt**2

        # Periodical boundary
        if self.x > max_x or self.x < 0:
            self.x = self.x - self.x // max_x * max_x
        if self.y > max_y or self.y < 0:
            self.y = self.y - self.y // max_y * max_y
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

        for atom in all_atoms:
            assert isinstance(atom, Mass)
            if atom == self:
                continue

            ax += self.k * (atom.x - self.x)
            ay += self.k * (atom.y - self.y)

        self.ax = ax
        self.ay = ay
        return ax, ay


def get_system_temperature(all_atoms, dimension, amount):
    sum = 0
    for atom in all_atoms:
        assert isinstance(atom, Mass)
        sum += 0.5 * (atom.vx ** 2 + atom.vy ** 2)
    return 2 * sum / dimension / amount


def temperature_adjust(T_tar):
    for atom in atom_list:
        atom.vx = atom.vx * ((T_eq / T_tar) ** 0.5)
        atom.vy = atom.vy * ((T_eq / T_tar) ** 0.5)


def move():
    plt.cla()
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    for atom in atom_list:
        atom.update_a(atom_list, prev=True)
        atom.update_a(atom_list, prev=False)
        atom.update_r(max_x, max_y)
        atom.update_v()
        plt.scatter(atom.x, atom.y, c='blue')

    plt.draw()
    plt.pause(0.2e-2)


atom_list = []
# Initialization
for i in range(num_of_atom):
    x0, y0 = random() * max_x, random() * max_y
    v0, theta0 = random() + 5, random() * 2 * pi
    atom_list.append(Mass(x0, y0, v0 * cos(theta0), v0 * sin(theta0), k=0.1))
    # plt.plot(x0, y0, c='blue')


while cur_t < t_max:
    move()
    if cur_t - cur_t // dt * dt > 100:
        T_cur = get_system_temperature(atom_list, 2, num_of_atom)
        if abs(T_cur - T_eq) > 1e-1:
            temperature_adjust(T_eq)
    cur_t += dt
