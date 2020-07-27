# Script iteratively solves the Manning-Strickler formula to claculate the normal flow depth associated with a
# certain discharge (for modifications go to if __name__ == "__main__" statement)


def reversed_mannings_fun(tar, args):
    """
    Inverted Manning-Strickler formula (solved for a target parameter tar)
    :param tar: target parameter (some kind of flow depth)
    :param args: Q, b, m_l, m_r, n_m, S_0
    :return: iterated target function
    """
    Q, b, m_l, m_r, n_m, S_0 = args
    area = ((((tar * m_l) + (tar * m_r) + b) + b) / 2) * tar
    perimeter = b + (tar * (m_l * m_l + 1) ** 0.5) + (tar * (m_r * m_r + 1) ** 0.5)
    ratio = area / perimeter
    return (Q * n_m / S_0 ** 0.5) - (area * ratio ** (2.0 / 3.0))


def solve(fun, x0, precision, args):
    """
    Solves fun as a function of x0 with precision and provided arguments
    :param fun: function to be solved
    :param x0: FLOAT initial guess of variable to solve for
    :param precision: FLOAT of step width of iteration
    :param args: LIST of variables defining discharge and flow cross section
    :return: FLOAT of iterative solution of x
    """
    last_x = x0
    next_x = last_x + 10 * precision  # must be different from last_x (ensure iteration)

    while abs(last_x - next_x) > precision:
        # get next solution
        next_y = fun(next_x, args)
        # # uncomment next line to print progress (slows down code)
        # print(str(last_x) + " > f(" next_x ") = " + str(next_y))
        last_x = next_x
        next_x = last_x - next_y / derivative(fun, last_x, precision, args)  # update estimate using N-R
    return next_x


def derivative(fun, x, delta_x, args):
    """
    evaluates and returns the derivative of fun(x) with step width delta_x and environment variables args
    :param fun: function
    :param x: FLOAT
    :param delta_x: FLOAT
    :param args: LIST(FLOAT)
    :return: FLOAT
    """
    return (fun(x + delta_x, args) - fun(x - delta_x, args)) / (2.0 * delta_x)


if __name__ == '__main__':
    # -- START MODIFICATION BLOCK: MODIFY INPUT PARAMETERS HERE
    Q = 15.5        # discharge in (m3/s)
    b = 5.1         # bottom channel width (m)
    m_left = 2.5    # left bank slope
    m_right = 2.5   # right bank slope
    n_m = 1/20      # Manning's n
    S_0 = 0.005     # channel slope
    init_value = .01  # initial value for iteration
    # -- END MODIFICATION BLOCK

    # prepare function input parameters
    args0 = [Q, b, m_left, m_right, n_m, S_0]
    # call the solver with user-defined initial value and step_width = init_value/10
    x_found = solve(reversed_mannings_fun, init_value, init_value / 10.0, args0)
    print("Iterated water depth = %.3f" % x_found)
