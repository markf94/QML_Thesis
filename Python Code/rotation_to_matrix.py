import numpy as np
import cmath
import math


def rotation_to_matrix(x=0, y=0, z=0):
    """
    Returns a unitary matrix that corresponds, in a useful but not unique way, to a rotation around
    the axis <x, y, z> by sqrt(x^2 + y^2 + z^2) radians.
    """
    s = math.copysign(1, -11*x + -13*y + -17*z)  # phase correction discontinuity on an awkward plane
    theta = math.sqrt(x**2 + y**2 + z**2)
    v = x * np.mat([[0, 1], [1, 0]]) +\
        y * np.mat([[0, -1j], [1j, 0]]) +\
        z * np.mat([[1, 0], [0, -1]])

    ci = 1 + cmath.exp(1j * s * theta)
    cv = math.sin(theta/2) * sinc(theta/2) - 1j * s * sinc(theta)

    return (np.identity(2) * ci - s * v * cv)/2


def sinc(x):
    """
    Returns sin(x)/x, but computed in a way that doesn't explode when x is equal to or near zero.
    sinc(0) is 1.
    """
    if abs(x) < 0.0002:
        return 1 - x**2 / 6
    return math.sin(x) / x

np.set_printoptions(precision=5, suppress=True)

print "I", rotation_to_matrix()
print "I_2", rotation_to_matrix(x=2*math.pi)
print "X", rotation_to_matrix(x=math.pi)
print "Y", rotation_to_matrix(y=math.pi)
print "Z", rotation_to_matrix(z=math.pi)
print "H", rotation_to_matrix(x=math.pi / math.sqrt(2), z = math.pi / math.sqrt(2))
print "sqrt_1(X)", rotation_to_matrix(x=math.pi/2)
print "sqrt_2(X)", rotation_to_matrix(x=-math.pi/2)
print "mygoal(Y)", rotation_to_matrix(y=1/8*math.pi)
