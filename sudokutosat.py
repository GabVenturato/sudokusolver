#!/usr/bin/python
# Gabriele Venturato - 2016/09/05
# Description: Transform a sudoku in DIMACS CNF format. In this way the output
#   can be used as input for a SATsolver.
# Version: 1.00 - 2016/09/05
# Input: list of list (see the code)
# Output: "sudoku.cnf" file

# ---------- FUNCTIONS ----------
# num: string, b: int
# return: int
def base_b_to_ten( num, b ):
    if len(num) == 0:
        return 0
    else:
        return int(num[-1]) + b * base_b_to_ten( num[:-1], b )

# x,y,z,n: int
# return: string
def sudoku_to_SAT( x, y, z, n ):
    x -= 1
    y -= 1
    z -= 1
    return str( base_b_to_ten( str(x)+str(y)+str(z), n ) +1 )
# helper for sudoku_to_SAT, same parameteres and return
def S( x, y, z, n ):
    return sudoku_to_SAT( x, y, z, n)

# Change Sign
# x: string
# return: string
def CS( x ):
    return str(-1*int(x))

# ---------- MAIN ----------
import math
n = 9 # sudoku dimension
srn = int(math.sqrt(n)) # square root of n, for sub-grids
cnf = "" # string for output

# INPUT
# 4x4
# sudoku = [[3,0,2,0],
#           [0,0,0,0],
#           [0,0,0,0],
#           [0,1,0,4]]

# 9x9
sudoku = [[1,8,0,0,3,9,0,4,0],
          [0,0,0,6,0,8,0,0,0],
          [0,0,0,0,0,0,0,5,9],
          [0,3,0,0,4,7,0,2,0],
          [6,0,0,0,0,0,7,1,0],
          [8,0,0,0,0,0,0,9,0],
          [2,0,6,1,0,0,0,0,0],
          [0,7,0,0,0,0,0,0,0],
          [4,0,0,0,0,5,2,0,0]]

# CONSTRAINTS
# There is at least one number in each entry
for x in range(1,n+1):
    for y in range(1,n+1):
        for z in range(1,n+1):
            cnf += S(x,y,z,n)+" "
        cnf += "0\n"

# Each number appears at most once in each column
for y in range(1,n+1):
    for z in range(1,n+1):
        for x in range(1,n):
            for i in range(x+1,n+1):
                cnf += CS( S(x,y,z,n) ) + " " + CS( S(i,y,z,n) ) + " 0\n"

# Each number appears at most once in each row
for x in range(1,n+1):
    for z in range(1,n+1):
        for y in range(1,n):
            for i in range(y+1,n+1):
                cnf += CS( S(x,y,z,n) ) + " " + CS( S(x,i,z,n) ) + " 0\n"

# Each number appears at most once in each sub-grid
for z in range(1,n+1):
    for i in range(0, srn):
        for j in range(0, srn):
            for x in range(1, srn+1):
                for y in range(1, srn+1):
                    for k in range(y+1, srn+1):
                        cnf += CS( S( (srn*i + x), (srn*j + y), z,n) ) + " " + CS( S( (srn*i + x), (srn*j + k), z,n) ) + " 0\n";

for z in range(1,n+1):
    for i in range(0, srn):
        for j in range(0, srn):
            for x in range(1, srn+1):
                for y in range(1, srn+1):
                    for k in range(x+1, srn+1):
                        for l in range(1, srn+1):
                            cnf += CS( S( (srn*i + x), (srn*j + y), z,n) ) + " " + CS( S( (srn*i + k), (srn*j + l), z,n) ) + " 0\n";

# KNOWN VALUES
for i in range(0,n):
    for j in range(0,n):
        if sudoku[i][j] > 0:
            cnf += S( i+1, j+1, sudoku[i][j], n ) + " 0\n"

# CNF HEADERS
cnf = "p cnf "+ str(n*n*n) + " " + str(cnf.count('\n')) + "\n" + cnf;

# FILE OUTPUT
out_file = open("sudoku.cnf","w")
out_file.write(cnf)
out_file.close()
