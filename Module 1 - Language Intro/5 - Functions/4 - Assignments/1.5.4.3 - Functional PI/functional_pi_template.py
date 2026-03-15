import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1  
    b = 1 / math.sqrt(2)
    t = 0.25
    p = 1
    while True:
        a_next = (a + b) / 2
        b_next = math.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2 * p

        pi_approximation = (a_next + b_next) ** 2 / (4 * t_next)

        if abs(math.pi - pi_approximation) < target_error:
            return pi_approximation

        a, b, t, p = a_next, b_next, t_next, p_next

    # change this so an actual value is returned
    return pi_approximation




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
