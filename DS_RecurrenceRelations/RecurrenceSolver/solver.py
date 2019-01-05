import sympy

class Solver:

    def __init__(self, general_sol, initials_dict):

        self._general_solution = general_sol
        self._initials_dict = initials_dict

        self._solve_alphas()

    def _solve_alphas(self):


        # equations = []
        # for i, c in self._initialConditions.items():
        #     eq = generalSolution - sympy.sympify("(%s)" % str(c))
        #     equations.append(eq.subs(ctx["n"], i))
        #
        # # Solve the system of equation
        # solve_symbols = [e for n, e in ctx.items() if n != "n"]
        # solutions = linsolve(equations, solve_symbols)
        #
        # if len(solutions) == 0:
        #     raise RecurrenceSolveFailed("No solution to the system of equations to find the alfas could be found.")
        #
        # solution = list(solutions)[0]
        #
        # # fill in the solution of the system
        # solved = generalSolution
        # for symbol, sub in zip(solve_symbols, list(solution)):
        #     solved = solved.subs(symbol, sub)
        #
        # return solved

        general_sol = self._general_solution
        ini_equations = list()
        symbols = {'n': sympy.var("n", integer = True)}
        # solve_symbols = [e for n, e in ctx.items() if n != "n"]

        for i, c in self._initials_dict.items():
            ini_eq = general_sol - sympy.sympify("({})".format(c), symbols)
            ini_eq = ini_eq.subs(symbols['n'], i)
            ini_equations.append(ini_eq)

        solutions = sympy.linsolve(ini_equations)

        print(solutions)