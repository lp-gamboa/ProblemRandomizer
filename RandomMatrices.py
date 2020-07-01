""" A module that produces 'nice' matrices. """
# import numpy as np 
from numpy import random as nr 
from sympy import *
from typing import Tuple

MatSize = Tuple[int, int]

def gen_matrix_rank(size: MatSize, rank, max_denom: int = 1, max_val: int = 3): 
    """ Generates a random (size[0])x(size[1]) matrix with given rank. """
    A, piv = zeros(size[0], size[1]), nr.choice(rank, size[1])
    for i in range(rank):
        A[i,piv[i]] = 1
        for j in range(piv[i]+1, size[1]):
            A[i,j] = nr.choice([a for a in range(-1*max_val + 1, max_val)])
    for i in range(size[0]):
        j = nr.choice(size[0], 3, replace=False)
        for k in j:
            if k!=i:
                A = A.elementary_row_op(op="n->n+km", row=i, row2=k, k=nr.choice(max_val)*nr.choice([-1,1]))
    return A
    
def gen_diagonal_matrix(size: int, det, max_denom: int =1): 
    """ Generates a random diagonal (size)x(size)-matrix with given determinant. """
    A, a, idx = eye(size), nr.choice(size), nr.choice(size, 2*int(size/3), replace=False)
    A = A.elementary_row_op(op="n->kn", row=idx[0], k=det)
    for x in range(int(size/3)):
        aux = nr.choice(3,2,replace=False)
        i, j = 3*x + aux[0], 3*x + aux[1]
        if det: 
            A = A.elementary_row_op(op="n->kn", row=i, k=max_denom)
            A = A.elementary_row_op(op="n->kn", row=j, k=Rational(1,max_denom))
        else: 
            A = A.elementary_row_op(op="n->kn", row=i, k=0)
    return A
    
def gen_int_triang_matrix(size: int, det, upper=True, max_val: int =7, max_denom: int = 1): 
    """ Generates a random triangular (size)x(size)-matrix with given determinant by taking linear combinations with integer coefficients of the rows of a diagonal matrix. """
    A, idx = gen_diagonal_matrix(size, det, max_denom), nr.randint(size)
    #A = A.elementary_row_op(op="n->kn", row=idx, k=det) # https://docs.sympy.org/latest/modules/matrices/matrices.html 
    for i in range(size):
        for j in range(i+1,size):
            A = A.elementary_row_op(op="n->n+km", row=i, row2=j, k=nr.choice(max_val)*nr.choice([-1,1]))
            # A[i,j] = nr.choice(max_val)*nr.choice([-1,1])
    if not upper:
        A = A.transpose()
    return A

def gen_sq_matrix(size: int, det, max_val: int =3, max_denom: int =1):
    """ Generates a random (size)x(size)-matrix with given determinant produced by taking linear combinations with integer coefficients of the rows of a triangular matrix. """
    A = gen_int_triang_matrix(size, det, upper=nr.random([0,1]), max_val=max_val)
    x = nr.choice(size, 2*int(size/3), replace=False)
    for i in x:
        A = A.elementary_row_op(op="n->kn", row=i, k=-1)
    perm = nr.choice(size, size, replace=False)
    for i in range(size):
        j = nr.choice([a for a in range(size)], int(size/2), replace=False)
        for k in j:
            if k!=perm[i]:
                c = nr.choice(max_val-1)+1
                A = A.elementary_row_op(op="n->n+km", row=perm[i], k=c, row2=k)
    return A 

def gen_sym_matrix(size: int, sym=True, max_val:int=3):
    """Generates a random integer valued (size)x(size)-matrix either symmetric or antisymmetric.""" 
    A = gen_int_matrix(size, 0, int(max_val/2)+1) 
    if sym: # True = Symmetric
        A = A + A.transpose()
        x = nr.choice(size, 2*int(size/3), replace=False)
        for i in x:
            A[i, i] = A[i, i]/2
    else: # False = Anti-symmetric
        A = A - A.transpose()
    return A 

