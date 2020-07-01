""" A module that produces 'nice' matrices. """

import numpy as np 
from numpy import random as nr 
import fractions as frac # https://docs.python.org/3/library/fractions.html 

def gen_int_matrix(size, det, max_val=3):
    """Generates a random (size)x(size)-matrix with given determinant produced by taking linear combinations with integer coefficients of the rows of a triangular matrix."""
    A, idx, aux = np.eye(size, dtype='int64'), nr.randint(size), nr.choice([0,1])
    A = A + frac.Fraction() # https://stackoverflow.com/questions/42577828/how-to-use-numpy-arrays-with-fractions 
    A[idx] = det*A[idx]
    for i in range(1,size):
        for j in range(i+1,size):
            A[i][j] = nr.choice(max_val)*nr.choice([-1,1])
    if aux:
        A = A.transpose()
    x = nr.choice(size, 2*int(size/3), replace=False)
    for i in x:
        A[i] = -1*A[i]
    perm = nr.choice(size, size, replace=False)
    for i in range(size):
        j = nr.choice([a for a in range(size)], int(size/2), replace=False)
        for k in j:
            if k!=perm[i]:
                c = nr.choice(max_val-1)+1
                A[perm[i]] = A[perm[i]] + c*A[k]
    return A + frac.Fraction()

def gen_int_sym_matrix(size, sym=True, max_val=3):
    """Generates a random integer valued (size)x(size)-matrix either symmetric or antisymmetric.""" 
    A = gen_int_matrix(size, 0, int(max_val/2)+1) 
    if sym: # True = Symmetric
        A = A + A.transpose()
        x = nr.choice(size, 2*int(size/3), replace=False)
        for i in x:
            A[i][i] = A[i][i]/2
    else: # False = Anti-symmetric
        A = A - A.transpose()
    return A 

