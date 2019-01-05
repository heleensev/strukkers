import fire
import os
import sys
import re
sys.path.append('../../strukkers')

from DS_RecurrenceRelations.RecurrenceSolver import raw_parser
from DS_RecurrenceRelations.RecurrenceSolver import equationbuilder
from DS_RecurrenceRelations.RecurrenceSolver import solver


class Recurrence:

    def __init__(self, inputdir):
        self._inputdir = inputdir

        self._inputstr = str()
        self._parsed = self._parse_input()
        self._equations = self._build_equation()



    def _open_file(self):
        try:
            with open(self._inputdir, 'r') as inputdir:
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
        equations = equationbuilder.EquationBuilder(parsed._recurrence, parsed._initials_dict)

        return equations

    def _solve_recur(self):
        self._closedform = None
        pass


    def _out_file(self):

        # check and create output directory
        outputdir = '../../ds_output_files'
        if not (os.path.exists(outputdir)):
            os.makedirs(outputdir)

        # build new output path
        prev_name, extension = os.path.splitext(self._inputdir)
        prev_name = prev_name + "-dir" + extension
        filename = os.path.join(outputdir, prev_name)

        # write file out to output path
        with open(filename, 'w') as out:
            out.write(self._closedform)

#
if __name__ == "__main__":
    fire.Fire(Recurrence)


# r = Recurrence("../../ds_assignment_files/comass03.txt")
