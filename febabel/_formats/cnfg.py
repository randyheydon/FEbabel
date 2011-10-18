"""
Contains a method for reading the configuration files of the Open Knee project.
See https://simtk.org/home/openknee
"""
from __future__ import with_statement

import ConfigParser, os.path
try: from cStringIO import StringIO
except: from StringIO import StringIO
from warnings import warn


SEPCHAR = ','
SEPCHAR2 = ';'

MATL_HEADER = 'material-'

DEFAULTS = 'defaults.cnfg'
INCL_KEY = '\nINCLUDE '



def _accrue_cnfg(filename, visited=frozenset()):
    "Returns the text of the given file, with all INCLUDEs swapped in."

    # Check if this file has been seen already, which would indicate a loop.
    if filename in visited:
        warn('INCLUDE loop found in "%s".  Breaking out.' % filename)
        return ''
    visited = visited.union([filename])

    with open(filename) as f:
        text = '\n%s' % f.read()

    incl_start = text.find(INCL_KEY)
    while incl_start != -1:
        # Parse out the filename, and find it relative to the current filename.
        fname_start = incl_start + len(INCL_KEY)
        incl_end = text.index('\n', fname_start)
        incl_file = os.path.join( os.path.dirname(filename),
            text[fname_start:incl_end].strip() )

        # Insert file, along with all of its includes, in place of INCLUDE line.
        text = '\n'.join( (text[:incl_start],
            _accrue_cnfg(incl_file, visited), text[incl_end:]) )

        incl_start = text.find(INCL_KEY)

    return text



def read(self, filename):
    """Read an Open Knee .cnfg file into the current problem."""

    with open(os.path.join(os.path.dirname(filename), DEFAULTS)) as f:
        text = '\n'.join(( f.read(), _accrue_cnfg(filename) ))
    cp = ConfigParser.SafeConfigParser()
    cp.readfp(StringIO(text), filename=filename)
