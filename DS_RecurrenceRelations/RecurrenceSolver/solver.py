import sympy

class Solver:

    def __init__(self, general_sol, homogeneous, nonhomogeneous, symbols_dict, initials_dict):

        self._general_solution = general_sol
        self._homogeneous = homogeneous
        self._non_homogeneous = nonhomogeneous
        self._symbols_dict = symbols_dict
        self._initials_dict = initials_dict

        self.homogeneous_solution = None
        self.solve()
        # self.alt_solve()



    def solve(self):

        self.homogeneous_solution = self._solve_alphas()

        pass


    def _solve_alphas(self):

        symbols_dict = self._symbols_dict

        general_sol = self._general_solution

        ini_equations = list()

        # solve_symbols = [e for n, e in ctx.items() if n != "n"]

        outputfile = open('solve_alpha_test.txt', 'w')
        outputfile.write('before subtracting\n'+str(general_sol)+ '\n\n')

        for i, c in self._initials_dict.items():

            ini_eq = general_sol - sympy.sympify('({})'.format(c))
            ini_eq = ini_eq.subs(symbols_dict['n'], int(i))

            outputfile.write(str(general_sol.subs(symbols_dict['n'], int(i))) + '= ' + str(i) +'\t' + 'i: ' + i + ' ' + 'c: '+ c + '\n___________________________________________________________________________________________________________\n\n')
            print(ini_eq)
            print(sympy.srepr(ini_eq))
            print('___________________________________________________________')
            ini_equations.append(sympy.sympify(ini_eq, symbols_dict))

        symbols_list = [v for k, v in symbols_dict.items() if k != 'n']

        outputfile.close()

        print(symbols_list)
        solutions = sympy.linsolve(ini_equations, symbols_list)

        if not solutions:
            print('no solutions found')
        sol = list(solutions)[0]

        for symbol, s in zip(symbols_list, list(sol)):
            general_sol = general_sol.subs(symbol, s)

        print('solution: {} '.format(str(general_sol)))



        return sympy.simplify(general_sol)



    def alt_solve(self):

        alphas = self.alt_solve_alphas()
        solution = self.alt_sub_alphas(alphas)

        print('solution: {}'.format(solution))

    def alt_solve_alphas(self):

        # alphas = {}
        # i = 0
        # for key in self.initials:
        #     variable = symbols("a{}".format(i))
        #     alpha = self.solve_initial(alphas, equation, key, variable)
        #     alphas[i] = alpha
        #     i = i + 1
        #
        # return alphas

        initials = self._initials_dict

        alphas = [v for k, v in self._symbols_dict.items() if k != 'n']
        solved_alphas = {}

        for n, alpha in zip(initials, alphas):
            solved_alpha = self.alt_solve_initial(solved_alphas, n, alpha)
            solved_alphas[alpha] = solved_alpha

        return solved_alphas

    def alt_solve_initial(self, solved_alphas, ini, alpha):
        #
        # n = symbols("n")
        # initial = self.initials[key]
        # inp = sympify(int(key))
        # out = sympify(initial)
        #
        # general = general.subs(n, inp)
        #
        # for a in alphas:
        #     alpha = symbols("a{}".format(a))
        #     general = general.subs(alpha, alphas[a])
        #
        # eq = Eq(general - out)
        # result = solve(eq, var)
        # return result[0]


        general = self._general_solution
        initials = self._initials_dict
        n_eq = initials[ini]

        # subsititute n in general equation for initial n
        n = sympy.var("n", integer=True)
        general_s = general.subs(n, int(ini))

        for s_alpha in solved_alphas:
            general_s = general_s.subs(s_alpha, solved_alphas[s_alpha])

        equation = sympy.Eq(general_s, int(n_eq))
        result = sympy.solve(equation, alpha, simplify=False, implicit=True)

        return result[0]


    def alt_sub_alphas(self, solved_alphas):

        general = self._general_solution

        for alpha in solved_alphas:
            general = general.subs(alpha, solved_alphas[alpha])

        solution = sympy.simplify(general)

        return solution
