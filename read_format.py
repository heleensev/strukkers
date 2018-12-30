from sys import argv, exit
import numpy as np
from sympy import *
import re

def main():
    inputpath = argv[1]
    file = read_file(inputpath)
    recurrence, split_formula = get_recurrence(file)
    initial_dict = get_initial_conditions(split_formula)
    constants = get_constants(recurrence)
    continuous, degrees = get_continuous(recurrence)
    degree = get_degree(degrees)
    char = get_char_eq(degree, constants, continuous)
    #answer = solve_lin_hom_deg2(initial_dict, constants ,continuous, degree, degrees)

def read_file(inputpath):
    input = open(inputpath, 'r')
    return input

def get_recurrence(file):
    formula = file.read().splitlines()

    formula = ' '.join(formula)
    split_formula = formula.split(',')
    # remove whitespaces
    split_formula = [x.strip() for x in split_formula]

    recur = formula.split(',')[0]

    if not recur.startswith('eqs'):
        print('error, input does not start with eqs')
    recur = recur.split('=')[2].strip().replace(' ', '')


    print("recurrence formula: %s "% recur)

    return recur, split_formula

def get_initial_conditions(split_formula):
    initials = [x for x in split_formula[1:]]

    if not initials[-1].endswith('];'):
        print('error, input does not end with ;]')

    initials[-1] = initials[-1][:-2]

    initial_dict = dict()

    # find inital conditions
    pat_n = r'(?<=\().+?(?=\))'
    pat_r = r'(?<=\= ).+?'
    for initial in initials:
        n = re.findall(pat_n, initial)
        r = re.findall(pat_r, initial)

        initial_dict[n[0]] = r[0] # add to dictionary

    print("dictionary for initial conditions:", initial_dict)

    return initial_dict

# function for reading standard form ca * s (n-d) + ca * s (n-d)
def get_constants(recur):
    # determine ca/an parts of formula
    pat_ca = r'(-*(\d\*)*s\(n-\d*\))'
    #pat_ca = r"(?<=\(n-)\d*(?=\))"
    all_constants  = re.findall(pat_ca, recur)
  #  print(all_constants)
 #   print(ca_an, len(ca_an)) #should incluce all seperate parts of equation with a length equal to the number of elements.

    # check if any constant coefficient can be found
    if all_constants:
        constants={}
        for x in range(1, len(all_constants)+1):
            current_part = all_constants[x-1]
            mi = current_part[0].index('*')
            current_constant = all_constants[x-1][0][0:mi] #This will only work if there is nothing else than the constant in front of the *
            if current_constant == '':
                constants["C_{0}".format(x)] = 1  #if multiplication sign is not found, set ca to 1
            else:
                constants["C_{0}".format(x)] = current_constant.strip('*')
    else:
        print('failed to find any constant coefficient/an')


    print('constant dict: %s' % constants)

    return constants

def get_continuous(recur):
    pat_ans = r'(?<=\(n-)\d*(?=\))'
    pat_ca = r'(s\(n([-|+])\d*\))'
    all_continuous = re.findall(pat_ca, recur)
   # print(all_continuous, len(all_continuous))

    if all_continuous:
        pat_ans = r'(?<=\(n-)\d*(?=\))'
        continuous = {}
        degrees = {}
        for x in range(1, len(all_continuous)+1):
            current_continuous = all_continuous[x - 1][0] # This will only work if there is nothing else than the constant in front of the *
            if current_continuous:
                continuous["continuous_{0}".format(x)] = current_continuous # if multiplication sign is not found, set ca to 1
                degrees["degree_{0}".format(x)] = re.findall(pat_ans,current_continuous)[0]
            else:
                print('Empty continuous part', x)
    else:
        print('failed to find any constant coefficient/an')

    print('continuous dict: %s' % continuous)
    print('degrees dict: %s' % degrees)

    return continuous, degrees



def get_degree(degrees):
    degree = max(degrees.values())
  #  pat_ans = r'(?<=\(n-)(\d)*(?=\))'
   # ans = re.findall(pat_ans, recur)
    # degree is highest of n-.. in formula
    #degree = int(max(ans))

    print("degree: %s\n" % degree)
    return int(degree)

def get_char_eq(degree, constants, continuous):
    num_of_con = len(constants)
    char_eq = "r^{0}".format(degree)

    for r in range(0, num_of_con):
    #    print(continuous["continuous_{}".format(r+1)])
        pat_ans = r'(?<=\(n-)\d*(?=\))'
        print(continuous["continuous_{}".format(r + 1)])
        print("degree", degree, "minus", "continuous",int(re.findall(pat_ans, continuous["continuous_{}".format(r + 1)])[0]))
        power = degree - int(re.findall(pat_ans, continuous["continuous_{}".format(r + 1)])[0])

        loopconst = constants["C_{}".format(r+1)]
        print("power", power)
        char_eq = char_eq + "-" + loopconst + "*r^" + str(power)
     #   print(char_eq)
    char_eq = char_eq.replace("--","+")
    print(factor(char_eq.replace("^","**")))
    print(char_eq)







#def solve_lin_hom_deg2(initials, constants, continu, degree, degrees):
    #check if linear = TRUE
    #check if homogeneous = TRUE
    #check if degree = 2
    # check_degree = None
   # print(type(degree))
   #  if degree == 2:
   #      check_degree = True
   #  else:
   #      print("Degree is not two")
   #  str1 = "r^"
   #  str2 = str(degree)
   #  str3 = "-"
   #  str4 = constants["C_1"]
   #  str5 = constants["C_2"]
   #  str6 = str(degree - int(degrees["degree_1"][0]))
   #  str7 = str(degree - int(degrees["degree_2"][0]))
   #  characteristic_eq = str1+str2 +str3+ str4+str1+str6+str3+str5+str1+str7
   #  if "--" in characteristic_eq:
   #      characteristic_eq = characteristic_eq.replace("--", '+')
   #  print(characteristic_eq)


# call standard form function
# do if condition or format check

main()
