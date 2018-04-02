from sympy import *
from lemmas.split import splitting
class LemmaCode(object):
    def isequal(input_exp):
        status = False
        newStr = str(input_exp)

        RHS = ""
        LHS = ""
        znak = ""

        bool = False
        splitted_array = splitting(newStr)
        LHS = splitted_array[0]
        RHS = splitted_array[1]
        znak = splitted_array[2]
        result = 'Wrong'
        if LHS.expand() == RHS.expand() and znak == '=':
            status = True
        if status == True:
            result = 'Correct'
        return result
    
