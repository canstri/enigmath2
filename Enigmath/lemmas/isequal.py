from sympy import *
from mpmath import *



def isequal(input_exp):
    status = False
    RHS = ""
    LHS = ""
    znak1 = ""
    znak2 = ""
    bool1 = False
    dannoe = input_exp

    if dannoe == '':
        return ('')

    for i in range(0, len(dannoe)):
        if (dannoe[i] == ">" and dannoe[i+1] == "=") or (dannoe[i] == "<" and dannoe[i+1] == "="):
            bool1 = True
            znak1 += dannoe[i] + dannoe[i+1]
            i = i+1
            continue
        elif dannoe[i] == ">" or dannoe[i] == "=" or  dannoe[i] == "<":
            bool1 = True
            znak1 += dannoe[i]
            
            continue
        if bool1 == True:
            RHS += dannoe[i]
        if bool1 == False:
            LHS += dannoe[i]

    if LHS == RHS:
        status = True
    
    result = 'Wrong'
    if status == True:
        result = 'Correct'
    return result

