import sympy
import re

class Analyzer:

    def __init__(self, recurrence, initials_dict):
        self._recurrence = recurrence
        self._initials_dict = initials_dict
        self._analyze_recur_type()

    def _analyze(self):
        try:
            self._analyze_recur_type()
        except:
            raise AttributeError


    def _analyze_recur_type(self):


        s = sympy.Function("s")
        n = sympy.var("n", integer=True)
        # i = sympy.Wild("i")

        homogenous = []
        nonhomogenous = []
        anc_dict = {}

        for arg in self._recurrence.args:
            # if s in subequation then it is homogeneous
            if arg.has(s):
                an_pat = r'(\d*)\*s\(n([-+]\d+)\)'
                match = re.match(an_pat, arg)
                if match:
                    c = match.group(1)
                    an = match.group(2)
                    if not c:
                        c = 1

                    anc_dict[an] = c
                else:
                    # raise error
                    pass
                homogenous.append(arg)

            else:
                nonhomogenous.append(arg)

        rec = self._recurrence
        # go = True
        #
        # for arg in rec.args:
        #     while go:
        #         if arg.func == sympy.Add:
        #             arg
        #         elif arg.has(n):
        #             go = False
        #
        #         else:
        #             go = False

        an_pat = r'(.*)\*s\(n([-+]\d+)\)'

        for arg in rec.args:
            if arg.has(n) and arg.has(s):
                sub = arg.args
                an = sub[0]
                match = re.findall(an_pat, str(arg))
                anc_dict[an] = match[1]


        self._degree = min(anc_dict.keys())
        self._anc_dict = anc_dict
        self.homogenous = homogenous
        self._nonhomogenous = nonhomogenous

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
        char_eq = r ** self._degree

        ordered = sorted(anc.keys())

        for i in ordered:
            char_eq = char_eq - anc[i] * r**(self._degree -i)


    def _create_general_solution(self):
        #characteristic equation get
        char_eq = self.char_eq

        #this function extracts the roots and puts them in a dictionary like; root:multiplicity
        rdict = sympy.roots(char_eq)
        #general_solution string, starts empty and is filled for each new characteristic equation
        general_solution = ""
        #for numbering alphas
        alphacount = 1
        #i = root, rdict[i] = multiplicity
        for i in rdict:
            if rdict[i] == 1:
                print("root " + str(i) + " has multiplicity equal to 1")
                if general_solution:
                    #if the general_solution is not empty, append stuff with a plus
                    general_solution += "+alpha_"+str(alphacount)+"*"+str(i)+"**n"
                else:
                    #if the general solution is empty, append stuff without a plus
                    general_solution += "alpha_"+str(alphacount) + "*"+str(i)+"**n"
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
                        if general_solution.endswith("("):
                            general_solution += "alpha_" + str(alphacount) + "_" + str(j) + "*" "n**" + str(m)
                        else:
                            general_solution += "+alpha_" + str(alphacount) + "_" + str(j) + "*" "n**"+ str(m)
                    alphacount += 1
                    general_solution += ")*("+i+")**n"
                else:
                    general_solution += "("
                    for m, j in enumerate(range(0,rdict[i])):
                        if general_solution.endswith("("):
                            general_solution += "alpha_" + str(alphacount) + "_" + str(j) + "*" "n**"+ str(m)
                        else:
                            general_solution += "+alpha_" + str(alphacount) + "_" + str(j) + "*" "n**"+ str(m)
                    alphacount += 1
                    general_solution += ")*("+i+")**n"


            self.general_solution = sympy.sympify(general_solution)
