import sympy
import re

class EquationBuilder:

    def __init__(self, recurrence, raw_recurrence, initials_dict):
        self._recurrence = recurrence
        self._raw_recurrence = raw_recurrence
        self._initials_dict = initials_dict
        self._general_solution = None
        self._char_eq = None
        self.nonhomogenous = None
        self._symbols_dict = None
        self.roots = None
        self._analyze_recur_type()
        self._create_char_eq()
        self._create_general_solution()
        self._build_equations()


    def _analyze(self):
        try:
            self._analyze_recur_type()
        except:
            raise AttributeError


    def _build_equations(self):

        particulars = []

        if self.nonhomogenous:
            particulars.append(self.particular_builder())


    def _analyze_recur_type(self):

        # s = sympy.Function("s")
        # n = sympy.var("n", integer=True)
        #
        # homogeneous = []
        # nonhomogeneous = []
        # anc_dict = {}
        # eq = self._raw_recurrence
        # rec = self._recurrence
        # an_pat = r'(.*)\**s\(n([-+]\d+)\)'
        # temp = ""
        # arg = ""
        # args = []
        # def paren_checker(str):
        #     return str.count("(") == str.count(")")
        # for i in eq:
        #     if i == "+"  and temp.find("s") and paren_checker(temp):
        #         arg += temp
        #         arg += i
        #         args.append(arg)
        #         arg = ""
        #         temp = ""
        #     elif i == "-" and temp.find("s") and paren_checker(temp):
        #         arg += temp
        #         arg += i
        #         args.append(arg)
        #         arg = ""
        #         temp = ""
        #     else:
        #         temp += i
        #
        # args.append(temp)
        #
        # #splitpos = [m.start() for m in re.finditer('[^n]-|\+', eq)]
        # #prev = -1
        # for i, arg in enumerate(args):
        #     if 's' in arg:
        #         homogeneous.append(arg)
        #         if 'n' in arg and 's' in arg:
        #             arg = str(arg).replace(' ', '')
        #             match = re.search(an_pat, arg)
        #             an = match.group(2)
        #             if match.group(1):
        #                 const = match.group(1).strip('*')
        #             else:
        #                 const = '1'
        #             if not an.isdigit() or not const.isdecimal(0):
        #                 print('Not a decimal')
        #                 print(arg)
        #                 print('an: {}, const: {}'.format(an, const))
        #             anc_dict[sympy.sympify(an)] = sympy.sympify(const)
        #     else:
        #         nonhomogeneous.append(arg)
        # print('ancdict: {}'.format(anc_dict))
        # self._degree = min(anc_dict.keys())
        # self._anc_dict = anc_dict
        # self.homogenous = homogeneous
        # self.nonhomogenous = nonhomogeneous

        s = sympy.Function("s")
        n = sympy.var("n", integer=True)

        homogeneous = []
        nonhomogeneous = []
        anc_dict = {}

        rec = self._recurrence
        an_pat = r'(.*)\**s\(n([-+]\d+)\)'

        for arg in rec.args:
            if arg.has(s):
                homogeneous.append(arg)
                if arg.has(n) and arg.has(s):
                    sub = arg.args
                    arg = str(arg).replace(' ', '')
                    match = re.search(an_pat, arg)
                    an = match.group(2)
                    if match.group(1):
                        const = match.group(1).strip('*')
                    else:
                        const = '1'
                    if not an.isdigit() or not const.isdecimal(0):
                        print('Not a decimal')
                        print(arg)
                        print('an: {}, const: {}'.format(an, const))
                    anc_dict[sympy.sympify(an)] = sympy.sympify(const)
            else:
                nonhomogeneous.append(arg)
        print('ancdict: {}'.format(anc_dict))
        self._degree = min(anc_dict.keys())
        self._anc_dict = anc_dict
        self.homogenous = homogeneous
        self.nonhomogenous = nonhomogeneous


    def _create_char_eq(self):
        r = sympy.Symbol('r')
        #
        # # build the dictionary where we link every constant to every a_n value
        # dicts = {}
        # self._dictBuilder(self._recurrence, dicts)
        #
        # # start building our new expression!
        # newExpr = r ** self._degree
        # for i in range(1, self._degree + 1):
        #     newExpr = newExpr - dicts.get(-i, 0) * r ** (self._degree - i)

        # anc = self._anc_dict
        #
        # r = sympy.Symbol('r')
        # degree = ((self._degree)*-1)
        # #char_eq = r ** degree
        # char_eq = 'r**{}'.format(degree)
        #
        # ordered_anc = sorted(anc.keys(), reverse=True)
        # ordered_const = ['({})'.format(anc[v]) for v in ordered_anc]
        #
        # for c, an in enumerate(range(0,len(ordered_anc))):
        #     char_eq = '{} - {} * r**{}'.format(char_eq, ordered_const[c], degree+ordered_anc[an])
        #     # char_eq = char_eq - ordered_const[c] * r**(degree +ordered_anc[an])
        #
        # print('charasteric equation: {}'.format(char_eq))
        # print(sympy.factor(char_eq))
        # print(sympy.roots(sympy.sympify(char_eq)))
        # print(len(sympy.roots(char_eq)))
        #
        # rdict = {s: m for (s, m) in sympy.roots(char_eq).items() if sympy.I not in s.atoms()}
        #
        # print('roots without imaginary: {}'.format(rdict))
        # self._char_eq = char_eq

        anc = self._anc_dict

        r = sympy.Symbol('r')
        degree = ((self._degree) * -1)
        char_eq = r ** degree

        ordered_anc = sorted(anc.keys(), reverse=True)
        ordered_const = [anc[v] for v in ordered_anc]

        for c, an in enumerate(range(0, len(ordered_anc))):
            char_eq = char_eq - ordered_const[c] * r ** (degree + ordered_anc[an])

        print('charasteric equation: {}'.format(char_eq))
        print(sympy.factor(char_eq))
        print(sympy.roots(char_eq))
        print(len(sympy.roots(char_eq)))

        rdict = {s: m for (s, m) in sympy.roots(char_eq).items() if sympy.I not in s.atoms()}

        print('roots without imaginary: {}'.format(rdict))
        self._char_eq = char_eq

    def _create_general_solution(self):

        symbols_dict = {'n': sympy.var("n", integer=True)}
        char_eq = self._char_eq
        #this function extracts the roots and puts them in a dictionary like; root:multiplicity

        rdict = sympy.roots(char_eq)

        rdict = {s: m for (s, m) in sympy.roots(char_eq).items() if sympy.I not in s.atoms()}
        # rdict = {sympy.simplify(s): m for (s,m) in rdict.items()}
        self.roots = rdict


        #general_solution string, starts empty and is filled for each new characteristic equation
        general_solution = ""
        #for numbering alphas
        alphacount = 1
        #i = root, rdict[i] = multiplicity
        for i in rdict:
            print('rdict i: {}'.format(rdict[i]))
            if rdict[i] == 1:
                alpha = "alpha_" + str(alphacount)
                alpha_eq = alpha + "*(" + str(i) + ")**n"
                symbols_dict[alpha] = sympy.var(alpha)

                print("root " + str(i) + " has multiplicity equal to 1")
                if general_solution:
                    #if the general_solution is not empty, append stuff with a plus
                    general_solution += "+" + alpha_eq
                else:
                    #if the general solution is empty, append stuff without a plus
                    general_solution += alpha_eq

                #add 1 to alphacount so that the variables are numbered correctly
                alphacount += 1
            #if rdict[i] is greater than 1, there are more than 1 multiplicities, the general solution is built differently
            elif rdict[i] > 1:
                print("root " + str(i) + " has multiplicity greater than 1")
                if general_solution:
                    general_solution += "+("
                    #clever use of enumerate function; m is used as a power to n, which always starts at 0, which means n is equal to 1 making it disposable
                    #j is used for counting the index of the alpha
                    for m, j in enumerate(range(0,rdict[i])):
                        alpha_mult = 'alpha_' + str(alphacount) + "_" + str(j)
                        alpha_mult_eq = alpha_mult + "*" "n**" + str(m)

                        symbols_dict[alpha_mult] = sympy.var(alpha_mult)

                        if general_solution.endswith("("):
                            general_solution += alpha_mult_eq

                        else:
                            general_solution += "+" + alpha_mult_eq
                    alphacount += 1
                    general_solution += ")*("+str(i)+")**n"
                else:
                    general_solution += "("
                    for m, j in enumerate(range(0,rdict[i])):
                        alpha_mult = 'alpha_' + str(alphacount) + "_" + str(j)
                        alpha_mult_eq = alpha_mult + "*" "n**" + str(m)

                        symbols_dict[alpha_mult] = sympy.var(alpha_mult)

                        if general_solution.endswith("("):
                            general_solution += alpha_mult_eq
                        else:

                            general_solution += "+" + alpha_mult_eq
                    alphacount += 1
                    general_solution += ")*("+str(i)+")**n"



        self._general_solution = sympy.sympify(general_solution, symbols_dict)
        self._symbols_dict = symbols_dict
        print()
        # return general_solution

    def particular_builder(self):
        fn = self.nonhomogenous
        # fn = [str(w).replace('*', '^') for w in fn if "*" in str(w)]
        symbols_dict = self._symbols_dict
        print('non homogeneous', fn)
        value_s = ""

        # tempfn = ""
        # print("args", fn[1])
        # for i in range(0,len(fn)):
        #    print(i)
        #    tempfn += str(fn[i]) + '+'

        # print(tempfn)

        # fntree = sympy.simplify(tempfn)
        # print('fntree', fntree.args)

        matching = [str(s)[:str(s).index("*")] for s in fn if "*n" in str(s)]
        matching2 = [str(s)[:str(s).index("*")] for s in fn if "*(n" in str(s)]

        #  print(matching2)

        if matching or matching2:
            value_s = max(matching + matching2)
            particular_end = "(" + str(value_s) + ')*n'
        else:
            value_s = 1
            particular_end = ""
            # print(value_s)

        print('particular end', particular_end)
        # print(self.roots)

        # roots = sympy.roots()
        if value_s in self.roots:
            multiplicity = self.roots.get(value_s)
            particular_start = 'n^' + str(multiplicity) + "*"
        else:
            particular_start = ""

        print("particular start", particular_start)

        # matching3 = [str(s)[str(s).index("n"):] for s in fn if "n" in str(s)]
        # powerlist = [str(s)[:s.index("*")+1] for s in fn if "*" in str(s)]
        matching3 = [str(s) for s in fn if "n" in str(s)]
        matching4 = [str(s) for s in matching3 if "**" not in str(s)[:str(s).index("n")]]
        # matching4 += [str(s) for s in fntree.args if "*n" in str(s)]

        matching5 = [str(s)[str(s).index("*") + 2:] for s in matching4 if "*" in str(s)]
        # print(matching4, 'm5', matching5)
        particular_mid = "(p_0"
        # symbols_dict["p_0"] = "p_0"
        if matching4:
            if not matching5:
                particular_mid += "+p_1*n"
        if matching5:
            for i in range(1, int(max(matching5)) + 1):
                particular_mid += "+p_" + str(i) + "n*" + str(i)
              #  symbols_dict["p_" + str(i)] = "p_" + str(i)
        # print(matching5)
        particular_mid += ")"

        general_particular_result = particular_start + particular_mid + particular_end
        print('general particular solution', general_particular_result)
      #  general_particular = sympy.simplify(particular_start + particular_mid + particular_end)
        #  print('simiplified', general_particular)
        self.general_particular_eq = general_particular_result
        self.particular_equation()

    def particular_equation(self):
        recurrence = str(self._recurrence)
        lhs = self.general_particular_eq
        tempfn = ""
        fntree = sympy.simplify(recurrence)
        # print('fntree', fntree.args)

        rhs = []
        for i in range(0, len(fntree.args)):
            current = str(fntree.args[i]).replace(' ', '')
            if 's' in current:
                if '(n' in current[current.index('s'):]:
                    # current.index[current.index("(n"):]
                    m = re.search('([+|-]\d*)', current[current.index("(n"):])
                    if m:
                        if len(rhs) is not 0:
                            rhs.append('+')
                        else:
                            pass
                        current_degree = m.group(1)
                        # print('current degree', current_degree)
                        current_replace = re.sub(r"n", '(n' + current_degree + ')', lhs)  # replaces the n in the general for the degree                       # print('found', current_degree)
                        # print('replace', fntree.args[i].replace('(n-\d*)', 'b'))
                        # print(re.sub(r"(s\(n-\d*\))", '(' + current_replace + ')', current))
                        rhs.append(re.sub(r"(s\(n-\d*\))", '(' + current_replace + ')', current))
                        # print(re.sub(r"s(n-\d*)", "", current))
                        # print(rhs)
            #  rhs.append(fntree.args[i].replace('n', 'b'))
            else:
                if len(rhs) is not 0:
                    rhs.append('+')
                    pass
                else:
                    pass
                rhs.append(current)

        rhs_string = ''
        for i in rhs:
            rhs_string += str(i)
        # print('lhs', lhs)
        general_particular_solution = lhs
        # print('rhs', rhs_string)

        ### works for p_0
        # print('types', type(lhs), type(rhs_string))
        equation = sympy.Eq(sympy.simplify(lhs), sympy.simplify(rhs_string))
        if 'p_0' in str(equation):
            value_p0 = sympy.solveset(equation, 'p_0')
            value_p0 = str(value_p0.args[0])

        print('p_0 is: ', value_p0)

        toreplace = str('(' + value_p0 + ')')
        lhs_p0 = lhs.replace('p_0', str(toreplace))

        rhs_string = sympy.simplify(rhs_string)
        rhs_p0 = str(rhs_string).replace('p_0', str(toreplace))

        eq_p0 = sympy.Eq(sympy.simplify(lhs_p0), sympy.simplify(rhs_p0))
        value_p1 = ''
        if eq_p0 == True:
            value_p1 = 0
            value_p1 = str(value_p1)

        eq_p1 = str(eq_p0).replace('p_1', str('(' + value_p1 + ')'))

        value_p0 = sympy.simplify(value_p0.replace('p_1', value_p1))
        value_p0 = str(value_p0)

        particular_solution = general_particular_solution.replace('p_0', value_p0)
        particular_solution = particular_solution.replace('p_1', value_p1)
        print(particular_solution)
        self.particular_solution = sympy.simplify(particular_solution)
        print('particular solution ', particular_solution)