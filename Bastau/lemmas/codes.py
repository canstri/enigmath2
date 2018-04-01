from sympy import *
class LemmaCode(object):
    def isequal(input_exp):
        status = False
        newStr = str(input_exp)

        RHS = ""
        LHS = ""
        znak1 = ""
        znak2 = ""

        bool = False
        for i in range(0, len(newStr)):
            if (newStr[i] == ">" and newStr[i+1] == "=") or (newStr[i] == "<" and newStr[i+1] == "="):
                bool = True
                znak1 += newStr[i] + newStr[i+1]
                i = i+1
                continue
            elif newStr[i] == ">" or newStr[i] == "=" or  newStr[i] == "<":
                bool = True
                znak1 += newStr[i]
                continue
            if bool == True:
                RHS += newStr[i]
            if bool == False:
                LHS += newStr[i]

        LHS = simplify(sympify(LHS).expand()) 
        RHS = simplify(sympify(RHS).expand())
        result = 'Wrong'
        if LHS == RHS:
            status = True
        if status == True:
            result = 'Correct'
        return result
        