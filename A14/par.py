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
    mag_list = []
    ene_list = []
    for res in res_list:
        cv_list.append(res.get()[1])
        t_list.append(res.get()[0])
        mag_list.append(res.get()[2])
        ene_list.append(res.get()[3])

    plt.cla()
    plt.scatter(t_list, cv_list, c='b')
    plt.xlabel('温度')
    plt.ylabel('热容')
    plt.savefig(f'cv-{in_list[0]}-{in_list[-1]}.png')
    plt.show()

    plt.cla()
    plt.scatter(t_list, mag_list)
    plt.xlabel('温度')
    plt.ylabel('平均磁化强度')
    plt.savefig(f'mag-{in_list[0]}-{in_list[-1]}.png')
    plt.show()

    plt.cla()
    plt.scatter(t_list, ene_list)
    plt.xlabel('温度')
    plt.ylabel('平均能量')
    plt.savefig(f'ene-{in_list[0]}-{in_list[-1]}.png')
    plt.show()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
