from __future__ import with_statement

from . import _formats


class FEproblem(object):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.elements = list()
        self.options = dict()


# Add in all reader/writer methods to FEproblem class.
FEproblem.read_inp = _formats.inp.read
FEproblem.write_feb = _formats.feb.write
