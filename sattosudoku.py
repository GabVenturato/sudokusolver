#!/usr/bin/python
# Gabriele Venturato - 2016/09/05
# Description: Use the SATsolver output in DIMACS CNF, to print the sudoku solution
#   in a more human readable way.
# Version: 1.00 - 2016/09/05
# Input: filename in command line
# Output: print in stdout

# ---------- FUNCTIONS ----------
# num: int, b: int
# return: string
def base_ten_to_b( num, b ):
    if num < b:
        return str(num)
    else:
        return base_ten_to_b( num//b, b ) + str( num%b )

# num: int, n: int
# return: dictionary where x is the row, y the column, and z the value in corresponding
#   position. these values star from zero, but sudoku human readable start from one.
def SAT_to_sudoku( num, n ):
    num = int(num)-1
    val = "000" + base_ten_to_b( num, n ) # needed always 3 characters
    val = val[-3:]  # take only last three
    return {'x': int(val[0]), 'y': int(val[1]), 'z': int(val[2])}

# initialize empty list of list. it will be filled with values read from file.
# n: int
def init_sudoku( n ):
    s = []
    for i in range(0,n):
        r = []
        for k in range(0,n):
            r.append(0)
        s.append(r)
    return s

# MAIN
import sys
n = 9 # sudoku dimension
sudoku = init_sudoku( n )

def main():
    filename = sys.argv[1]
    f = open(filename, 'rU')
    lines = f.readlines()
    if lines[0] != 'SAT\n': # first line says if it is satisfiable
        print('Sudoku impossible to solve.')
    else:
        line = lines[1].split()
        for s in line:
            if( int(s) > 0 ):
                position = SAT_to_sudoku( int(s), n )
                sudoku[ position['x'] ][ position['y'] ] = position['z']+1
    f.close()

    # print the sudoku solution
    print("SUDOKU SOLUTION:\n")
    for line in sudoku:
        for entry in line:
            print(str(entry)+" "),
        print("\n")

if __name__ == '__main__':
    main()
