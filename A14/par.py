import multiprocessing
from ising import ising_core
from matplotlib import pyplot as plt


def main():
    pool = multiprocessing.Pool(2)

    in_list = [1.5 + 0.1 * x for x in range(15)]
    res_list = []

    for t in in_list:
        res = pool.apply_async(ising_core, args=(t,))
        res_list.append(res)

    pool.close()
    pool.join()

    cv_list = []
    t_list = []
    for res in res_list:
        cv_list.append(res.get()[1])
        t_list.append(res.get()[0])

    plt.cla()
    plt.scatter(t_list, cv_list, c='b')
    plt.savefig(f'cv-{in_list[0]}-{in_list[-1]}.png')
    plt.show()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
