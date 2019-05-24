from numpy import random, sqrt
from matplotlib import pyplot as plt

dx = 1
init_range = 30
cord_range = 100
number_of_atoms = 1000


def move(cord: tuple) -> tuple:
    direction = random.choice([0, 1, 2, 3])
    ret = ()
    if direction == 0:
        ret += (cord[0] + dx,)
        ret += (cord[1],)
    elif direction == 1:
        ret += (cord[0],)
        ret += (cord[1] + dx,)
    elif direction == 2:
        ret += (cord[0] - dx,)
        ret += (cord[1],)
    elif direction == 3:
        ret += (cord[0],)
        ret += (cord[1] - dx,)

    return ret


def is_adjacent(cord: tuple, seed: set) -> bool:
    t_0 = (cord[0] + dx, cord[1])
    t_1 = (cord[0] - dx, cord[1])
    t_2 = (cord[0], cord[1] + dx)
    t_3 = (cord[0], cord[1] - dx)

    return t_0 in seed or t_1 in seed or t_2 in seed or t_3 in seed


def main() -> set:
    seed = {(0, 0)}
    for i in range(number_of_atoms):
        p = (random.randint(-init_range, init_range), random.randint(-init_range, init_range))
        while sqrt(p[0] ** 2 + p[1] ** 2) <= cord_range:
            if is_adjacent(p, seed):
                seed.add(p)
                break

            p = move(p)

    return seed


def fig_out(seed: set):
    for point in seed:
        plt.scatter(point[0], point[1], c='blue')

    plt.savefig('dla.png')
    plt.show()


seed_res = main()
fig_out(seed_res)
