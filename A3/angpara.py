import numpy as np
from numpy import linalg

# Size: 2*2*3.84
# Angular parameter
par1 = 7.3591994181087100E-02  # Parallel bottom -> top
par2 = 2.3160200145472900E-01  # Orthogonal bottom -> side
par3 = 2.3868285729087200E-01  # Orthogonal side -> side
par4 = 2.8138220056958200E-01  # Parallel side -> side
par5 = 1.2062604242433800E-01  # Orthodonal side -> bottom
# Absorption rate
a = 0.9

coefficient_mat = np.mat([[1 / (a - 1), par5, par5, par5, par5, par1],
                          [par2, 1 / (a - 1), par3, par4, par3, par2],
                          [par2, par3, 1 / (a - 1), par3, par4, par2],
                          [par2, par4, par3, 1 / (a - 1), par3, par2],
                          [par2, par3, par4, par3, 1 / (a - 1), par2],
                          [par1, par5, par5, par5, par5, 1 / (a - 1)]], dtype="float64")

constant_vec = np.array([1 / (a - 1), 0, 0, 0, 0, 0])
result = linalg.solve(coefficient_mat, constant_vec)  # Outbound flux
s = result[1:] / (1 - a)
print(f'Outbound: {result}\nInbound: {s}')
