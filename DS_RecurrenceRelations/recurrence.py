import fire
import os
import sys

sys.path.append('/home/sevvy/Documents/data science/ds/computer assignment/recurrence_relation')

from DS_RecurrenceRelations.RecurrenceSolver import raw_parser
from DS_RecurrenceRelations.RecurrenceSolver import analyzer
from DS_RecurrenceRelations.RecurrenceSolver import solver


class Recurrence:

    def __init__(self, inputdir):
        self._inputdir = inputdir
        # self._outputdir = outputdir

        self._inputstr = str()
        self._parsed = self._parse_input()
        self._analyzer = self._analyze()



    def _open_file(self):
        try:
            with(self._inputdir, 'r') as inputdir:
                self._inputstr = open(inputdir, 'r')

        except FileNotFoundError:
            print('Input directory is not valid')
            exit(1)

    def _parse_input(self):
        import re

        # remove whitespaces
        input_str = self._inputstr.replace(' ','')
        # check standard format
        eq_pattern = r'eqs\:=\[s\(.*\)=.*,+.*\];'
        match = re.findall(eq_pattern, input_str, re.S | re.M)
        if not match:
            print('warning: input file not of expected form')

        parsed = raw_parser.Parser(self._inputstr)
        return parsed

    def _analyze(self):
        parsed = self._parsed
        analyzed = analyzer.Analyzer(parsed._recurrence, parsed._initials_dict)

        return analyzed

    def _solve_recur(self):
        self._closedform = None
        pass


    def _out_file(self):
        if not (os.path.exists(self._outputdir)):
            os.makedirs(self._outputdir)

        with open(self._outputdir, 'w') as out:
            out.write(self._closedform)


if __name__ == "__main__":
    fire.Fire(Recurrence)