import sympy
import re

class EquationBuilder:

    def __init__(self, recurrence, initials_dict):
        self._recurrence = recurrence
        self._initials_dict = initials_dict

        self._char_eq = None
        self.nonhomogenous = None
        self._general_solution = None
        self._symbols_dict = None
        self._analyze_recur_type()
        self._build_equations()
        self._create_char_eq()
        self._create_general_solution()

    def _analyze(self):
        try:
            self._analyze_recur_type()
        except:
            raise AttributeError


    def _build_equations(self):

        particulars = []
        for part in self.non_homogeneous:
            particulars.append(self.particular_builder())

    def _analyze_recur_type(self):

        s = sympy.Function("s")
        n = sympy.var("n", integer=True)

        homogeneous = []
        nonhomogeneous = []
        anc_dict = {}

        rec = self._recurrence
        an_pat = r'(.*)\*s\(n([-+]\d+)\)'

        for arg in rec.args:
            if arg.has(s):
                homogeneous.append(arg)
                if arg.has(n) and arg.has(s):
                    sub = arg.args
                    const = sub[0]
                    arg = str(arg).replace(' ', '')
                    match = re.search(an_pat, arg)
                    an = match.group(2)
                    anc_dict[int(an)] = int(const)
            else:
                nonhomogeneous.append(arg)

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

        anc = self._anc_dict

        r = sympy.Symbol('r')
        degree = ((self._degree)*-1)
        char_eq = r ** degree

        ordered_anc = sorted(anc.keys(), reverse=True)
        ordered_const = [anc[v] for v in ordered_anc]

        for c, an in enumerate(range(0,len(ordered_anc))):
            char_eq = char_eq - ordered_const[c] * r**(degree +ordered_anc[an])

        self._char_eq = char_eq


    def _create_general_solution(self):

        symbols_dict = {'n': sympy.var("n", integer=True)}
        char_eq = self._char_eq
        #this function extracts the roots and puts them in a dictionary like; root:multiplicity
        rdict = sympy.roots(char_eq)
        #general_solution string, starts empty and is filled for each new characteristic equation
        general_solution = ""
        #for numbering alphas
        alphacount = 1
        #i = root, rdict[i] = multiplicity
        for i in rdict:
            if rdict[i] == 1:
                alpha = "alpha_" + str(alphacount)
                alpha_eq = alpha + "*" + str(i) + "**n"
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

            sol = sympy.sympify(general_solution, symbols_dict)
            print(sol.args)
            print(sympy.srepr(sol))
            print('__________________________________________________')


            self._general_solution = sympy.sympify(general_solution, symbols_dict)
            self._symbols_dict = symbols_dict
            # return general_solution

    def particular_builder(self):

        pass