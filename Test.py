P = 1000      # kN
B = 2.0       # m
L = 3.0       # m
e = 0.3       # m

A = B * L
M = P * e

sigma_max = (P / A) + (6 * M / (B * L**2))
sigma_min = (P / A) - (6 * M / (B * L**2))

print(sigma_max, sigma_min)
