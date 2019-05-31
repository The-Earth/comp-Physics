from matplotlib import pyplot as plt
import numpy as np


def random_flip(arr: np.ndarray):
    y_choice = np.random.randint(0, arr.shape[0])
    x_choice = np.random.randint(0, arr.shape[1])
    flip_one(arr, (y_choice, x_choice))

    return y_choice, x_choice


def flip_one(arr: np.ndarray, cord: tuple):
    if arr[cord[0], cord[1]] == 1:
        arr[cord[0], cord[1]] = -1
    elif arr[cord[0], cord[1]] == -1:
        arr[cord[0], cord[1]] = 1
    else:
        raise ValueError


def total_energy(arr: np.ndarray) -> float:
    beta = -1
    energy = 0
    total_length = arr.shape[0] * arr.shape[1]
    for ind in range(total_length):
        x_1 = ind % arr.shape[1]
        y_1 = ind // arr.shape[0]
        if x_1 == arr.shape[1] - 1 and y_1 != arr.shape[0] - 1:
            energy -= beta * arr[y_1, x_1] * arr[y_1 + 1, x_1]
        elif x_1 != arr.shape[1] - 1 and y_1 == arr.shape[0] - 1:
            energy -= beta * arr[y_1, x_1] * arr[y_1, x_1 + 1]
        elif x_1 == arr.shape[1] - 1 and y_1 == arr.shape[0] - 1:
            pass
        else:
            energy -= beta * (arr[y_1, x_1] * arr[y_1 + 1, x_1] + arr[y_1, x_1] * arr[y_1, x_1 + 1])

    return energy


size = 20
steps = int(2e3)
accept_para = 0.8
p_size = 20

crystal = np.zeros(shape=(size, size), dtype='int8')

# Initialize

for i in range(size):
    for j in range(size):
        crystal[i, j] = np.random.choice([-1, 1])
        if crystal[i, j] == 1:
            plt.scatter(j, i, s=p_size, c='b')
        elif crystal[i, j] == -1:
            plt.scatter(j, i, s=p_size, c='r')
plt.savefig('crystal_init.png')
plt.show()

energy_list = [total_energy(crystal)]
cur_step = 1
while cur_step < steps:
    flipped = random_flip(crystal)
    cur_energy = total_energy(crystal)
    if cur_energy < energy_list[-1]:
        energy_list.append(cur_energy)
        cur_step += 1
    else:
        p = np.exp(-accept_para * (cur_energy - energy_list[-1]))  # Accept by chance
        if np.random.random() < p:
            energy_list.append(cur_energy)
            cur_step += 1
        else:
            flip_one(crystal, flipped)

plt.cla()
for i in range(size):
    for j in range(size):
        if crystal[i, j] == 1:
            plt.scatter(j, i, s=p_size, c='b')
        elif crystal[i, j] == -1:
            plt.scatter(j, i, s=p_size, c='r')
        else:
            raise ValueError

plt.savefig('crystal.png')
plt.show()

plt.cla()
plt.plot(list(range(steps)), energy_list, c='b')
plt.savefig('energy.png')
plt.show()
