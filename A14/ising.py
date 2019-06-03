from matplotlib import pyplot as plt
import numpy as np

size = 20
steps = int(2e5)
p_size = 30


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
    energy = 0
    total_length = arr.shape[0] * arr.shape[1]
    for ind in range(total_length):
        x_1 = ind % arr.shape[1]
        y_1 = ind // arr.shape[0]
        if x_1 != arr.shape[1] - 1:
            energy -= arr[y_1, x_1] * arr[y_1, x_1 + 1]
        else:
            energy -= arr[y_1, x_1] * arr[y_1, 0]

        if y_1 != arr.shape[0] - 1:
            energy -= arr[y_1, x_1] * arr[y_1 + 1, x_1]
        else:
            energy -= arr[y_1, x_1] * arr[0, x_1]

        if x_1 != 0:
            energy -= arr[y_1, x_1] * arr[y_1, x_1 - 1]
        else:
            energy -= arr[y_1, x_1] * arr[y_1, -1]

        if y_1 != 0:
            energy -= arr[y_1, x_1] * arr[y_1 - 1, x_1]
        else:
            energy -= arr[y_1, x_1] * arr[0, x_1]

    return energy / 2


def delta_energy(arr: np.ndarray, target: tuple) -> float:
    delta = 0
    y, x = target
    new_val = arr[target]
    old_val = 1 if new_val == -1 else -1

    if x != arr.shape[1] - 1:
        delta += ((-arr[y, x + 1] * new_val) - (-arr[y, x + 1] * old_val))
    else:
        delta += ((-arr[y, 0] * new_val) - (-arr[y, 0] * old_val))
    if y != arr.shape[0] - 1:
        delta += ((-arr[y + 1, x] * new_val) - (-arr[y + 1, x] * old_val))
    else:
        delta += ((-arr[0, x] * new_val) - (-arr[0, x] * old_val))
    if x != 0:
        delta += ((-arr[y, x - 1] * new_val) - (-arr[y, x - 1] * old_val))
    else:
        delta += ((-arr[y, -1] * new_val) - (-arr[y, -1] * old_val))
    if y != 0:
        delta += ((-arr[y - 1, x] * new_val) - (-arr[y - 1, x] * old_val))
    else:
        delta += ((-arr[-1, x] * new_val) - (-arr[-1, x] * old_val))

    return delta


def ising_core(T):
    accept_para = 1 / T
    crystal = np.zeros(shape=(size, size), dtype='int8')

    # Initialize

    for i in range(size):
        for j in range(size):
            crystal[i, j] = np.random.choice([-1, 1])
            # if crystal[i, j] == 1:
            #     plt.scatter(j, i, s=p_size, c='b')
            # elif crystal[i, j] == -1:
            #     plt.scatter(j, i, s=p_size, c='r')
    # plt.savefig('crystal_init.png')
    # plt.show()

    energy_list = [total_energy(crystal)]
    cur_step = 1

    # Cv calc
    sample_start = 0
    sampled = 0

    while cur_step < steps:
        flipped = random_flip(crystal)
        dE = delta_energy(crystal, flipped)
        cur_energy = energy_list[-1] + dE
        if dE < 0:
            energy_list.append(cur_energy)
            cur_step += 1
        else:
            p = np.exp(-accept_para * dE)  # Accept by chance
            if np.random.random() < p:
                energy_list.append(cur_energy)
                cur_step += 1
            else:
                flip_one(crystal, flipped)

        # energy_monitor = energy_list[-50:]
        # if max(energy_monitor) - min(energy_monitor) < 30 and not sampled:
        #     sample_start = cur_step
        #     print(cur_step)
        #     sampled = 1

    # Calculate Cv
    sample = energy_list[-50000:]
    sample_ave_sqr = (sum(sample) / len(sample)) ** 2
    sample_sqr_ave = sum([x ** 2 for x in sample]) / len(sample)
    Cv = (size ** 2) / (T ** 2) * (sample_sqr_ave - sample_ave_sqr)

    # plt.cla()
    # for i in range(size):
    #     for j in range(size):
    #         if crystal[i, j] == 1:
    #             plt.scatter(j, i, s=p_size, c='b')
    #         elif crystal[i, j] == -1:
    #             plt.scatter(j, i, s=p_size, c='r')
    #         else:
    #             raise ValueError
    # plt.savefig('crystal.png')
    # plt.show()

    plt.cla()
    plt.plot(list(range(steps)), energy_list, c='b')
    plt.savefig(f'./pic/energy-{T}.png')
    print(T, 'done')

    return T, Cv


if __name__ == '__main__':
    pass
