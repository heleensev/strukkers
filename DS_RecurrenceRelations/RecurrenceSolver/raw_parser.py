import re
from sympy import *

class Parser:

    def __init__(self, inputstr):
        self._inputstr = inputstr

        recur_form, split_form = self._split_input()
        self._recurrence = self._get_recurrence(recur_form)
        self._initials_dict = self._get_initial_conditions(split_form)

    def _split_input(self):

        inputstr = self._inputstr

        splitstr = inputstr.splitlines()
        splitstr = ' '.join(splitstr).replace(' ', '')

        # split input string into recurrence formula and initial conditions
        split_formula = splitstr.split(',')

        raw_recur_str = split_formula[0]

        recur_form = raw_recur_str.split('=')[2]
        split_form = split_formula[1:]

        return recur_form, split_form

    def _get_recurrence(self, recur_form):

        # check what the recurrence relation equals to (usually s(n) )
        rec_eq_pat = r'(?<=eqs\:=\[s).*(?=\=.*)'
        match = re.search(rec_eq_pat, recur_form)
        if not match:
            pass
        else:
            match = match.group()
            rec_eq = match.lstrip('(').rstrip(')')
            if not rec_eq == 'n':
                pass

        print(recur_form)
        recursplit = recur_form.split('=')[2:]

        self._symbols = {
            "s": sympy.Function("s"),
            "n": sympy.var("n", integer=True)
        }

        recursplit = re.sub("\^", "**", recursplit)
        recurrence = sympify(recursplit, self._symbols)

        return recurrence

    def _get_initial_conditions(self, split_form):

        # remove ]; from input form
        split_form[-1] = split_form[-1].rstrip('];')
        init_pat = r's\(\d{1,3}\)=\d{1,3}'

        match = re.findall(init_pat, split_form, re.M)
        if not match:
            pass
        else:
            initials_dict = dict()

            for init in match:
                split_ini = init.split('=')
                init_key = split_ini.strip('(').split(')')
                initials_dict[init_key] = split_ini[1]

        return initials_dict


