import fire
import os
from .raw_parser import Parser
from .analyzer import Analyzer

class Recurrence:

    def __init__(self, inputdir, outputdir):
        self._inputdir = inputdir
        self._outputdir = outputdir

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

        parsed = Parser(self._inputstr)
        return parsed

    def _analyze(self):
        analyzed = Analyzer()

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