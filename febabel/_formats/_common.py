"""
Data and structures that are useful to multiple format handling modules.
"""


# String used to combine filename and setname when reading in a file.
SETSEP = ':'
# Strings used to denote a file's default nodeset and elementset.
NSET = 'allnodes'
ESET = 'allelements'



class ValsDict(dict):
    """A standard dict, except that iteration goes over values instead of keys.
    This makes it usable in FEproblem.sets, while also allowing key-based
    access to its values."""
    def __iter__(self):
        return self.itervalues()
