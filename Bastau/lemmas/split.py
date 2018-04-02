from sympy import *
from mpmath import *

def splitting(string):
    znak = ""
    lhs = ""
    rhs = ""
    met = False
    skip = False
    for i in range (0, len(string)):
        if skip == True:
            skip = False
            continue
        if (string[i] == ">" and string[i+1] == "=") or (string[i] == "<" and string[i+1] == "="):
            met = True
            znak = string[i] + string[i+1]
            #i += 2
            skip = True
            continue
        elif string[i] == ">" or string[i] == "<" or string[i] == "=":
            met = True
            znak = string[i]
            #i += 2
            skip = False
            continue
        if met == False:
            lhs += string[i]
        else:
            rhs += string[i]
    
    lhs = sympify(lhs)
    rhs = sympify(rhs)
    result_array = [lhs, rhs, znak]
    return result_array
