import numpy as np


def cal(configure):
    fi_alpha = configure['cadr_value'] / 3600
    A_alpha = 0.5
    delta_x = configure['room_side'] / 3
    number = configure['incense_number']
    ac_location = configure['ac_loc']
    wall = configure['wall']

    # ------------------------------------------------------------
    v_alpha = fi_alpha / A_alpha
    v_tol = v_alpha
    Q = 2.8 * delta_x * v_tol   # Q = q_tol

    a = np.array([
        [2 * Q,    -Q,     0,    -Q,
         0,     0,     0,     0,     0],
        [-Q, 3 * Q,    -Q,     0,    -
         Q,     0,     0,     0,     0],
        [0,    -Q, 2 * Q,     0,     0,    -Q,     0,     0,     0],
        [-Q,     0,     0, 3 * Q,    -
         Q,     0,    -Q,     0,     0],
        [0,    -Q,     0,    -Q, 4 *
         Q,    -Q,     0,    -Q,     0],
        [0,     0,    -Q,     0,    -Q,
         3 * Q,     0,     0,    -Q],
        [0,     0,     0,    -Q,     0,
         0, 2 * Q,    -Q,     0],
        [0,     0,     0,     0,    -Q,
         0,    -Q, 3 * Q,    -Q],
        [0,     0,     0,     0,     0,    -Q,     0,    -Q, 2 * Q],
    ])

    b = np.array([
        0.8 * 0.03 * 1000000 * number /
        (2.8 * 3600 * (delta_x * 3) ** 2), 0, 0, 0, 0, 0, 0, 0, 0
    ])
    b = b.reshape([9, 1])

    x = np .zeros([9, 1])
    ac = 0.9 * fi_alpha
    for n in range(1, 10):
        if ac_location == n:
            a[n - 1, n - 1] += ac

    for wall_number in range(1, 13):
        if wall_number in wall:
            if wall_number < 7:
                small, big = (wall_number + ((wall_number - 1) // 2) - 1,
                              wall_number + ((wall_number - 1) // 2))

            else:
                small, big = wall_number - 7, wall_number - 4
            a[small, small] -= Q
            a[small,   big] += Q
            a[big,   big] -= Q
            a[big, small] += Q

    for i in range(n):
        if not (np.any(a[i, :])) == True:
            a[i, i] = 10**(-16)

    def pivot(k):
        p = k
        big = abs(a[k, k]/s[k])
        for ii in range(k+1, n):
            dummy = abs(a[ii, k]/s[ii])
            if dummy > big:
                big = dummy
                p = ii
        if p != k:
            for jj in range(k, n):
                dummy = a[p, jj]
                a[p, jj] = a[k, jj]
                a[k, jj] = dummy
            dummy = b[p, 0]
            b[p, 0] = b[k, 0]
            b[k, 0] = dummy
            dummy = s[p]
            s[p] = s[k]
            s[k] = dummy

    def elimination():
        for k in range(n-1):
            pivot(k)
            for i in range(k+1, n):
                factor = a[i, k]/a[k, k]

                for j in range(k, n):
                    a[i, j] = a[i, j]-factor*a[k, j]
                b[i, 0] = b[i, 0]-factor*b[k, 0]

    def substitute():
        x[n-1] = b[n-1, 0]/a[n-1, n-1]
        for i in range(n-2, -1, -1):
            sum = 0
            for j in range(i+1, n):
                sum = sum+a[i, j]*x[j]
            x[i] = (b[i, 0]-sum)/a[i, i]
        number = 0

        for i in range(len(x)):
            value = round(x[i][0], 2)
            if value > 10e6:
                value = f'{value:.3e}'
                x[i][0] = value
            else:
                value = f'{value}'
                x[i][0] = value

        return x

    s = np.zeros([n])
    er = 0
    for i in range(n):
        s[i] = abs(a[i, 0])
        for j in range(1, n):
            if abs(a[i, j]) > s[i]:
                s[i] = abs(a[i, j])

    elimination()
    return substitute()
