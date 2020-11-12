import math as m


def calc_discharge(b, h, k_st, m, S):
    pass


def solver(*args, **kwargs):
    pass


if __name__ == '__main__':
    # input parameters
    Q = 15.5        # discharge in (m3/s)
    b = 5.1         # bottom channel width (m)
    m = 2.5         # bank slope
    n_m = 1/20      # Manning's n
    S_0 = 0.005     # channel slope

    # call the solver with user-defined channel geometry and discharge
    h_n = solver(Q, b, n_m=n_m, m=m, S0=S_0)
