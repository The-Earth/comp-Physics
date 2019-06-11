from math import sqrt, pi
import multiprocessing


def distance(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def orth_ang(hori: float, itsc: float, verti: float, dx, dy, dz, x_start) -> float:
    ret = 0
    da1, da2 = dx * dy, dy * dz

    cur_h_x = x_start

    while cur_h_x < hori:
        cur_h_y = dy / 2
        while cur_h_y < itsc:
            cur_v_y = dy / 2
            while cur_v_y < itsc:
                cur_v_z = dz / 2
                while cur_v_z < verti:
                    cur_dis = distance(cur_h_x, cur_h_y, 0, 0, cur_v_y, cur_v_z)
                    cos1 = distance(cur_h_x, cur_h_y, 0, 0, cur_v_y, 0) / cur_dis
                    cos2 = distance(0, cur_h_y, 0, 0, cur_v_y, cur_v_z) / cur_dis
                    ret += cos1 * cos2 * da1 * da2 / (pi * (cur_dis ** 2))

                    cur_v_z += dz

                cur_v_y += dy

            cur_h_y += dy

        print(cur_h_x)
        cur_h_x += dx

    return ret


def main():
    pool = multiprocessing.Pool(2)

    hori, itsc, verti = 2, 2, 2
    div = 200
    dx, dy, dz = hori / div, itsc / div, verti / div

    res_list = []
    res_list.append(pool.apply_async(orth_ang, args=(hori / 2, itsc, verti, dx, dy, dz, dx / 2)))
    res_list.append(pool.apply_async(orth_ang, args=(hori, itsc, verti, dx, dy, dz, hori / 2 + dx / 2)))

    pool.close()
    pool.join()

    tot = 0
    for res in res_list:
        tot += res.get()

    print(tot / (hori * itsc))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
