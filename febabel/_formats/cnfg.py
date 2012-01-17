"""
Contains a method for reading the configuration files of the Open Knee project.
See https://simtk.org/home/openknee
"""
from __future__ import with_statement

import ConfigParser, os.path, itertools
try: from cStringIO import StringIO
except: from StringIO import StringIO
from warnings import warn

import sys
if sys.version > '3':
    cp_kwargs = {'strict':False}
else:
    cp_kwargs = {}


from .. import problem, materials as mat, constraints as con
from ._common import SETSEP, NSET, ESET

SEPCHAR = ','
SEPCHAR2 = ';'

MATL_HEADER = 'material-'

DEFAULTS = 'defaults.cnfg'
INCL_KEY = '\nINCLUDE '


# Relates each material type name that can appear in a cnfg file to a function
# that takes the parameters dict and returns a material object.
# TODO: Density support for all materials.
# TODO: Cover more materials.  Only these four are currently used in configs.
f = float
material_read_map = {
    'rigid': lambda p: mat.Rigid(
        map( f,p['com'].split(SEPCHAR) ), f(p['density']) ),
    'Mooney-Rivlin': lambda p: mat.MooneyRivlin(
        f(p['c1']), f(p['c2']), f(p['k']) ),
    'Fung Orthotropic': lambda p: mat.FungOrthotropic(
        f(p['e1']), f(p['e2']), f(p['e3']),
        f(p['g12']), f(p['g23']), f(p['g31']),
        f(p['v12']), f(p['v23']), f(p['v31']),
        f(p['c']), f(p['k']), mat.NodalOrientation(
            (int(p['axis1'])-1, int(p['axis2'])-1),
            (int(p['axis1'])-1, int(p['axis3'])-1) ) ),
    'trans iso Mooney-Rivlin': lambda p: mat.TransIsoElastic(
        f(p['c3']), f(p['c4']), f(p['c5']),
        f(p['lambda_star']), mat.NodalOrientation(
            (int(p['fiber direction node 1'])-1, int(p['fiber direction node 2'])-1),
            # Second edge is arbitrary for a trans iso material.
            (int(p['fiber direction node 1'])-1, int(p['fiber direction node 2'])) ),
        mat.MooneyRivlin( f(p['c1']), f(p['c2']), f(p['k']) ) ),
}



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
    geo_default = '%s:'%geo_files[0] if len(geo_files)==1 else ''


    # The string that precedes all objects created in the cnfg file.
    filename_key = os.path.basename(filename)


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


    # Create materials and apply to sets.
    materials = dict()
    for s in cp.sections():
        if s.startswith(MATL_HEADER):
            params = dict(cp.items(s))
            matl = material_read_map[ params['type'] ](params)

            # Get the set name to which the material is being applied.
            # If the given set name already specifies its originating file, go
            # with it.  Otherwise (in a single-geometry config), add the geo
            # file name to the set name.
            eset = s[len(MATL_HEADER):]
            materials[eset] = matl # For lookup when setting rigid constraints.
            if not eset.startswith(geo_default):
                eset = geo_default + eset
            for elem in self.sets[eset]:
                elem.material = matl


    # Set constraints.
    # First generate loadcurves.
    loadcurves = dict()
    for n,curve in cp.items('loadcurves'):
        loadcurves[n] = con.LoadCurve( dict(
            map(float, pt.split(SEPCHAR)) for pt in curve.split(SEPCHAR2) ),
            # FIXME: Should not assume that lc option contains a valid
            # interpolation method.  Use a dict lookup instead.
            interpolation=cp.get('options','lc') )

    # Then go through rigid body constraints for each step.
    step_duration = cp.getfloat('solver','time_steps') * cp.getfloat('solver','step_size')
    bodies = dict()
    for cnt in itertools.count():
        secn = 'step %s' % (cnt+1)
        if not cp.has_section(secn): break
        step_start = step_duration * cnt

        for body,constr_string in cp.items(secn):
            # If this body hasn't been seen in any step so far, give it an
            # empty SwitchConstraint for each of its 6 degrees of freedom.
            switches = bodies.setdefault( body,
                [con.SwitchConstraint({}) for _ in xrange(6)] )

            # Add the appropriate constraint at the current time for each DOF.
            for switch,constr in zip(switches, constr_string.split(SEPCHAR)):
                if 'free' in constr:
                    switch.points[step_start] = con.free
                elif 'fixed' in constr:
                    switch.points[step_start] = con.fixed
                elif 'force' in constr:
                    _, lc, m = constr.split(SEPCHAR2)
                    switch.points[step_start] = con.Force(
                        loadcurves[lc.strip()], float(m) )
                elif 'prescribed' in constr:
                    _, lc, m = constr.split(SEPCHAR2)
                    switch.points[step_start] = con.Displacement(
                        loadcurves[lc.strip()], float(m) )

    # And apply each assembled switch constraint to the corresponding degree of
    # freedom of the corresponding rigid body.
    # NOTE: In the cnfg file, constraints must be ordered as x,y,z,Rx,Ry,Rz.
    # If that is not followed, here is where it will screw up.
    for body,switches in bodies.iteritems():
        matl = materials[body]
        for dof,switch in zip( ('x','y','z','Rx','Ry','Rz'), switches ):
            matl.constraints[dof] = switch


    # Create rigid interfaces.
    rigid_int = set()
    self.sets[SETSEP.join((filename_key, 'rigid_int'))] = rigid_int

    for name,value in cp.items('rigid_int'):
        # If value is set to False (or other equivalent value), ignore it.
        try:
            if not cp.getboolean('rigid_int', name):
                continue
        except ValueError: pass

        nset, body = map(str.strip, value.split(SEPCHAR))
        rigid_int.add(con.RigidInterface(
            materials[body], self.sets[geo_default + nset] ))


    # Create contact interfaces.
    contact = set()
    self.sets[SETSEP.join((filename_key, 'contact'))] = contact
    # Prepare contact settings.
    contact_settings = dict(cp.items('contact_settings'))
    if contact_settings['type'] == 'facet-to-facet sliding':
        friction = 0; biphasic = False; solute = False
    elif contact_settings['type'] == 'sliding2':
        friction = 0; biphasic = True; solute = False
    elif contact_settings['type'] == 'sliding3':
        friction = 0; biphasic = True; solute = True
    else:
        warn('Do not recognize contact type "%s".  Assuming facet-to-facet.' %
             contact_settings['type'])
        friction = 0; biphasic = False; solute = False
    del contact_settings['type']

    for name,value in cp.items('contact'):
        # If value is set to False (or other equivalent value), ignore it.
        try:
            if not cp.getboolean('contact', name):
                continue
        except ValueError: pass

        master, slave = map(str.strip, value.split(SEPCHAR))
        contact.add(con.SlidingContact(
            self.sets[geo_default + master], self.sets[geo_default + slave],
            friction, biphasic, solute, contact_settings ))


    # TODO: Something with solver settings.
    # TODO: Figure out contact.
    # TODO: Generate springs.


problem.FEproblem.read_cnfg = read
