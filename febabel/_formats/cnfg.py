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
    # FIXME: Go through all sets created by each geo file, not just allnodes?
    nodeset = set()
    for f in geo_files:
        nodeset.update( self.sets[SETSEP.join((f, NSET))] )
    nodeset = list(nodeset)

    # Get transform points from config.
    trans = dict()
    for k in ('medial_f_cond', 'lateral_f_cond', 'proximal_femur',
        'distal_femur', 'proximal_tibia'):
        trans[k] = np.array(map( float,
            cp.get('transform', k).split(SEPCHAR) ))
    q_angle = float(cp.get('transform', 'q_angle'))
    scale = float(cp.get('options', 'scale'))

    # Determine the three axes of the femoral coordinate system.
    q_angle_RM = [[1,  0,  0],
        [0,  np.cos(q_angle), -np.sin(q_angle)],
        [0,  np.sin(q_angle),  np.cos(q_angle)]]
    mech_axis = np.dot( q_angle_RM,
        trans['proximal_femur'] - trans['distal_femur'] )
    ant_post_axis = np.cross( mech_axis,
        trans['lateral_f_cond'] - trans['medial_f_cond'] )
    flex_axis = np.cross( ant_post_axis, mech_axis )
    # Normalize axes
    e1_prime = flex_axis / np.linalg.norm( flex_axis )
    e2_prime = ant_post_axis / np.linalg.norm( ant_post_axis )
    e3_prime = mech_axis / np.linalg.norm( mech_axis )

    # Rotation and scaling matrix to convert coordinate system.
    RM = np.array( [e1_prime, e2_prime, e3_prime] ) / scale
    # Translation vector to bring to new origin.
    trans_vec = -(trans['distal_femur'] + trans['proximal_tibia']) / 2
    # Now transform all those points!
    # All points are offset by the translation vector.  The resulting point
    # matrix is transposed, so each column represents one point.  This allows
    # all points to be simultaneously multiplied by the rotation matrix.  The
    # result is then transposed again to bring it back to one point per row.
    new_nodeset = np.dot( RM, (np.array(nodeset) + trans_vec).T ).T

    # Set all nodes to their new coordinates.
    for node, pos in zip(nodeset, new_nodeset):
        node.x, node.y, node.z = pos


    # TODO: Something with solver settings.
    # TODO: Generate loadcurves.
    # TODO: Generate constraints and their switches, then apply to bodies.
    # TODO: Generate materials, then apply to elements.
    # TODO: Figure out contact.
    # TODO: Generate springs.
