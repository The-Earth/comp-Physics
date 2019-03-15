import numpy as np
from numpy import linalg

# Size: 2*2*3.84
# Angular parameter
par1 = 1.20866658758691e-1
par2 = 6.85895888785527e-2
par3 = 2.81382200569582e-1
par4 = 1.2062604242338e-1
par5 = 2.3868285729087e-1
# Absorption rate
a = 0.9

coefficient_mat = np.mat([[1 / (a - 1), par2, par2, par2, par2, par1],
                          [par4, 1 / (a - 1), par5, par3, par5, par4],
                          [par4, par5, 1 / (a - 1), par5, par3, par4],
                          [par4, par3, par5, 1 / (a - 1), par5, par4],
                          [par4, par5, par3, par5, 1 / (a - 1), par4],
                          [par1, par2, par2, par2, par2, 1 / (a - 1)]]).transpose()

constant_vec = np.array([1 / (a - 1), 0, 0, 0, 0, 0])
result = linalg.solve(coefficient_mat, constant_vec)

print(sum(result))
