"""
Core design calculations for eccentric footing
"""

def area(B, L):
    return B * L


def moment(P, e):
    return P * e


def section_modulus(B, L, axis="x"):
    """
    axis = 'x' (bending along L)
    axis = 'y' (bending along B)
    """
    if axis == "x":
        return B * L**2 / 6
    elif axis == "y":
        return L * B**2 / 6
    else:
        raise ValueError("axis must be 'x' or 'y'")


def soil_pressure(P, B, L, e, axis="x"):
    """
    Returns sigma_max, sigma_min (kN/m^2)
    """
    A = area(B, L)
    M = moment(P, e)
    Z = section_modulus(B, L, axis)

    sigma_avg = P / A
    sigma_bending = M / Z

    sigma_max = sigma_avg + sigma_bending
    sigma_min = sigma_avg - sigma_bending

    return sigma_max, sigma_min
