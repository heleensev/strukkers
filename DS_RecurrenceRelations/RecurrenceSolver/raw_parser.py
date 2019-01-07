import re as rex
import sympy


class Parser:

    def __init__(self, inputstr):
        self._inputstr = inputstr

        self._check_input()
        recur_form, initials = self._split_input()
        self._recurrence = self._get_recurrence(recur_form)
        self._initials_dict = self._get_initial_conditions(initials)

    def _check_input(self):

        # remove newlines and whitespaces
        input_str = self._inputstr.splitlines()
        input_str = ''.join(input_str).replace(' ','')
        # check standard format
        eq_pattern = r'eqs\:=\[s\(.*\)=.*,+.*\];'
        match = rex.findall(eq_pattern, input_str, rex.S | rex.M)
        if not match:
            print('warning: input file not of expected form')

        print(input_str)

    def _split_input(self):

        inputstr = self._inputstr

        splitstr = inputstr.splitlines()
        splitstr = ' '.join(splitstr).replace(' ', '')

        # check what the recurrence relation equals to (usually s(n) )
        rec_eq_pat = r'(?<=eqs\:=\[s).*?(?=\=.*)'
        match = rex.search(rec_eq_pat, inputstr)
        if not match:
            pass
        else:
            match = match.group()
            rec_eq = match.lstrip('(').rstrip(')')
            if not rec_eq == 'n':
                print('equation does not equal n, but: {}'.format(rec_eq))

        # split input string into recurrence formula and initial conditions
        split_formula = splitstr.split(',')

        raw_recur_str = split_formula[0]

        recur_form = raw_recur_str.split('=')[2]
        initials = split_formula[1:]

        return recur_form, initials

    def _get_recurrence(self, recur_form):


        self._symbols = {
            "s": sympy.Function("s"),
            "n": sympy.var("n", integer=True)
        }

        recurrence = recur_form.replace("^", "**")
        recurrence = sympy.sympify(recurrence, self._symbols)

        return recurrence

    def _get_initial_conditions(self, split_form):

        split_str = ''.join(split_form)

        init_pat = r's\(\d{1,3}\)=\d{1,3}'

        match = rex.findall(init_pat, split_str, rex.M)
        if not match:
            raise Exception("Could not find initial conditions")

        initials_dict = dict()

        for init in match:
            init_match = rex.search(r's\((\d+)\)=(\d+)', init)
            init_key = init_match.group(1)
            init_val = init_match.group(2)

            initials_dict[init_key] = init_val

        return initials_dict


