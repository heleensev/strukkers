import fire
import os
import sys
import signal
import time
import re
from sympy.abc import y
sys.path.append('../strukkers')

from DS_RecurrenceRelations.RecurrenceSolver import raw_parser
from DS_RecurrenceRelations.RecurrenceSolver import equationbuilder
from DS_RecurrenceRelations.RecurrenceSolver import solver


class Timeout(Exception):
    pass

class Recurrence:

    def __init__(self, inputfile=None, loop=False):
        self._inputfile = inputfile

        self._inputdir = "../ds_assignment_files"
        self._inputstr = str()
        self._closedform = None
        self.symbols_dict = None
        self.homogeneous = None
        self.nonhomogeneous = None

        if loop:
            self._loop_directory()
        else:
            self._process_relation()

    def _process_relation(self):

       # try:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        print('Processing...\n')
        self._parsed = self._parse_input()
        self._general_solution = self._build_equation()
        self._solved = self.try_solve(self._solve_recur, 10)
        self._write_output()
       # except Exception as e:
       #     exc_type, exc_obj, exc_tb = sys.exc_info()
       #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
       #     print(exc_type, fname, exc_tb.tb_lineno)

    def _loop_directory(self):

        for filename in os.listdir(self._inputdir):
            print(filename)
            filename = os.path.join(self._inputdir, filename)
            self._inputfile = filename
            self._process_relation()


    def _open_file(self):
        try:
            with open(self._inputfile, 'r') as inputdir:
                return inputdir.read()

        except FileNotFoundError:
            print('Input directory is not valid')
            exit(1)

    def _parse_input(self):
        inputstr = self._open_file()

        parsed = raw_parser.Parser(inputstr)

        print(parsed._recurrence)
        print(parsed._initials_dict)
        return parsed


    def _build_equation(self):
        parsed = self._parsed
        builder = equationbuilder.EquationBuilder(parsed._recurrence, parsed._raw_recurrence, parsed._initials_dict)
        general_solution = builder._general_solution

        self.homogeneous = builder.homogenous
        self.nonhomogeneous = builder.nonhomogenous
        self.symbols_dict = builder._symbols_dict
        self.particular = builder.particular_solution

        return general_solution

    def _solve_recur(self):
        initials = self._parsed._initials_dict
        symbols = self.symbols_dict
        homogenous = self.homogeneous
        nonhomogenous = self.nonhomogeneous
        solved = solver.Solver(self._general_solution, homogenous, nonhomogenous, symbols, initials)
        self._homogeneous_sol = solved.homogeneous_solution

    def _make_outputfile(self):

        output = 'sdir := n -> {} + {};'.format(self._homogeneous_sol, self.particular)
        return output


    def _write_output(self):

        output = self._make_outputfile()

        # check and create output directory
        outputdir = '../ds_output_files'
        if not (os.path.exists(outputdir)):
            os.makedirs(outputdir)

        # build new output path
        prev_name = os.path.basename(self._inputfile)
        filename, file_extension = os.path.splitext(prev_name)
        filename = filename + '-dir.txt'
        filename = os.path.join(outputdir, filename)

        # write file out to output path
        with open(filename, 'w') as out:
            out.write(output)

    def try_solve(self, func, t):
        def timeout_handler(signum, frame):
            raise Timeout()

        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(t)  # triger alarm in 3 seconds

        try:
            t1 = time.clock()
            func()
            t2 = time.clock()

        except Timeout:
            print('{} timed out after {} seconds'.format(func.__name__, t))
            return None
        finally:
            signal.signal(signal.SIGALRM, old_handler)

        signal.alarm(0)
        return t2 - t1


#
if __name__ == "__main__":
    fire.Fire(Recurrence)


# r = Recurrence("../../ds_assignment_files/comass03.txt")