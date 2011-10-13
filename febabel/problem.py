from __future__ import with_statement

from . import _formats


class FEproblem(object):
    """A class to contain an entire finite element problem description."""

    def __init__(self):
        self.elements = set()
        self.options = dict()


    def get_nodes(self):
        "Returns the set of all nodes found in elements."
        nodes = set()
        for e in self.elements:
            nodes.update(iter(e))
        return nodes


    def get_materials(self):
        "Returns the set of all materials found in elements."
        return set(e.material for e in self.elements)


# Add in all reader/writer methods to FEproblem class.
FEproblem.read_inp = _formats.inp.read
FEproblem.write_feb = _formats.feb.write
