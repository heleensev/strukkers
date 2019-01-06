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

    def solve(self):

        self.homogeneous_solution = self._solve_alphas()

        for part in self._non_homogeneous:

        pass


    def _solve_alphas(self):

        symbols_dict = self._symbols_dict

        general_sol = self._general_solution

        ini_equations = list()

        # solve_symbols = [e for n, e in ctx.items() if n != "n"]

        for i, c in self._initials_dict.items():
            ini_eq = general_sol - sympy.sympify('({})'.format(c))
            ini_eq = ini_eq.subs(symbols_dict['n'], int(i))
            #
            print(ini_eq)
            print(sympy.srepr(ini_eq))
            print('___________________________________________________________')
            ini_equations.append(sympy.sympify(ini_eq, symbols_dict))

        symbols_list = [v for k, v in symbols_dict.items() if k != 'n']

        print(symbols_list)
        solutions = sympy.linsolve(ini_equations, symbols_list)

        sol = list(solutions)[0]

        for symbol, s in zip(symbols_list, list(sol)):
            general_sol = general_sol.subs(symbol, s)

        return sympy.simplify(general_sol)



    def _solve_non_homogenous(self):

        def _solveNonHomogeneous(self, realRoots, homogeneous, nonHomogenous, generalSolution, ctx):
            """
            get the closed form equation for a non-homogeneous recurrence relation
            given the general solution for the associated homogeneous recurrence

            Args:
                realRoots (dict of sympy expr: int): The roots of the characteristic equation with multiplicities
                homogeneous (sympy expression): The associated homogenous equation
                nonHomogenous (sympy expression): The part of the equation that makes the recurrence non homogenous
                generalSolution (sympy expression): The general solution for the associated homogeneous recurrence
                ctx (dict of string: sympy symbol): The context of the general solution

            Returns:
                sympy expression: The closed form solved
            """

            solveableRecurrence = self._recurrence - sympy.sympify("s(n)", self._sympy_context)

            guess = 0
            guess_ctx = {
                "n": sympy.var("n", integer=True)
            }

            # Check if non homogenous part is exponential in n
            is_exponential = self._is_exponential(nonHomogenous, False)

            if is_exponential:
                guess_ctx["a"] = sympy.var("a")
                guess_ctx["b"] = sympy.var("b")
                guess_ctx["c"] = sympy.var("c")

                guess = sympy.sympify("a + b**n + c", guess_ctx)

            solve_symbols = [e for n, e in guess_ctx.items() if n != "n"]
            for i in range(0, self._degree + 1):
                guessFilled = guess.subs(guess_ctx["n"], guess_ctx["n"] - i)
                replaceFunction = sympy.sympify("s(n-%d)" % i, self._sympy_context).simplify()
                solveableRecurrence = solveableRecurrence.subs(replaceFunction, guessFilled)

            solutions = list(sympy.solve(solveableRecurrence, solve_symbols))
            if len(solutions) == 0:
                msg = "Couldn't solve a guess for a particular solution."
                #raise RecurrenceSolveFailed(msg)

            solutions = list(solutions[0])

            # The solution might contain free variables so we replace those with 0
            solution_just_symbols = [s for s in solutions if s in solve_symbols]
            for i in range(0, len(solutions)):
                for s in solution_just_symbols:
                    solutions[i] = solutions[i].subs(s, 0)

                solutions[i] = solutions[i].simplify()

            # replace the solution for the guess into the solveable recurrence
            particularSolution = solveableRecurrence
            for symbol, sub in zip(solve_symbols, solutions):
                particularSolution = particularSolution.subs(symbol, sub)

            result = particularSolution + generalSolution

            return self._calculateClosedFromGeneralSolution(result, ctx)