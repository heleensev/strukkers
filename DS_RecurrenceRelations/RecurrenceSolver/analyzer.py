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

        ordered = sorted(anc.values())

        for i in range(0, ordered):
            char_eq = char_eq - anc[ordered[i]]