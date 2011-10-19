"""
Contains a method for reading the configuration files of the Open Knee project.
See https://simtk.org/home/openknee
"""
from __future__ import with_statement

import ConfigParser, os.path
try: from cStringIO import StringIO
except: from StringIO import StringIO
from warnings import warn

import sys
if sys.version > '3':
    cp_kwargs = {'strict':False}
else:
    cp_kwargs = {}


from ._common import SETSEP, NSET, ESET

SEPCHAR = ','
SEPCHAR2 = ';'

MATL_HEADER = 'material-'

DEFAULTS = 'defaults.cnfg'
INCL_KEY = '\nINCLUDE '



def _accrue_cnfg(filename, visited=frozenset()):
    "Returns the text of the given file, with all INCLUDEs swapped in."
    # FIXME: This would really be better if it just used cp.read on each file.

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
    import numpy as np

    with open(os.path.join(os.path.dirname(filename), DEFAULTS)) as f:
        text = '\n'.join(( f.read(), _accrue_cnfg(filename) ))
    cp = ConfigParser.SafeConfigParser(**cp_kwargs)
    cp.readfp(StringIO(text), filename=filename)


    # Read in listed geometry source files.
    geo_files = map(str.strip, cp.get('options', 'mesh').split(SEPCHAR))
    for f in geo_files:
        self.read(os.path.join(os.path.dirname(filename),f))

    # If only one geometry file is specified, then its sets can be accessed
    # in the config file directly by set name.  Otherwise, all sets must be
    # accessed as "filename:setname".
    # Note that str.startswith('') is always True.
    geo_default = geo_files[0] if len(geo_files)==1 else ''


    # Collect all nodes in the geometry source files.
    nodeset = set()
    for f in geo_files:
        nodeset.update( self.sets[SETSEP.join((f, NSET))] )
    nodeset = list(nodeset)
    nodearray = np.array(nodeset).T

    # TODO: Transform all nodes involved in this config.


    # TODO: Something with solver settings.
    # TODO: Generate loadcurves.
    # TODO: Generate constraints and their switches, then apply to bodies.
    # TODO: Generate materials, then apply to elements.
    # TODO: Figure out contact.
    # TODO: Generate springs.
