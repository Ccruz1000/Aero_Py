# Imported Functions
import numpy as np
import math
import scipy.integrate as integrate
from scipy.interpolate import interp1d

# User Defined Functions
from Function_File import integrate


def thin_airfoil(alpha, camber, x_y, h):
    # Convert alpha to radians
    alpha = alpha / 180 * math.pi

    # Interpolate function for camber line
    camber_line = interp1d(x_y, camber)

    # Determine derivative of camber line
    dx_y = np.zeros(np.shape(x_y))
    # Take derivative at first point using forward step method
    dx_y[0] = ((camber_line(x_y[0] + h) - camber_line(x_y[0])) / h)
    # Take derivative at last point using backward step method
    dx_y[-1] = ((camber_line(x_y[-1]) - camber_line(x_y[-1] - h)) / h)
    # Take derivative at points between first and last using central difference formula
    for i in range(2, len(x_y) - 2):
        dx_y[i] = ((camber_line(x_y[i] + h) - camber_line(x_y[i] - h))/(2*h))

    # Convert x to theta
    theta = np.arccos(1 - 2 * x_y[:])

    # Compute integrals for each coefficient
    a0 = alpha - 1.0 / math.pi * integrate(theta, dx_y)
    a1 = 2 / math.pi * integrate(theta, np.multiply(dx_y, np.cos(theta)))
    a2 = 2 / math.pi * integrate(theta, np.multiply(dx_y, np.cos(2 * theta)))

    # Calculate lift and moment coefficient
    cl = math.pi * (2 * a0 + a1)
    cm = math.pi / 4 * (a2 - a1)

    return cl, cm
