from .constraints import Constrainable
# FIXME: Density belongs in every material.



class Material(object):
    "Base material object."

    def _store(self, params):
        del params['self']
        # TODO: Have parameters as a dict linked to attributes?
        self.parameters = params.keys()
        for k,v in params.iteritems():
            setattr(self, k, v)



# TODO: Docstrings showing strain-energy functions.
class LinearIsotropic(Material):
    def __init__(self, E, v):
        self._store(locals())

class NeoHookean(Material):
    def __init__(self, E, v):
        self._store(locals())

class HolmesMow(Material):
    def __init__(self, E, v, beta):
        self._store(locals())

# TODO: Handle incomp enforcement (laugon, atol).
class MooneyRivlin(Material):
    def __init__(self, c1, c2, k):
        self._store(locals())

class VerondaWestmann(Material):
    def __init__(self, c1, c2, k):
        self._store(locals())

class ArrudaBoyce(Material):
    def __init__(self, mu, N, k):
        self._store(locals())

class Ogden(Material):
    # TODO: FEBio has both incomp Ogden and "Ogden unconstrained".  How deal?
    def __init__(self, ci, mi, k):
        self._store(locals())

class Rigid(Material, Constrainable):
    # TODO: FEBio has E and v for "auto-penalty contact formulation".  Need?
    def __init__(self, center_of_mass=None, density=None):
        Constrainable.__init__(self, 'x','y','z','Rx','Ry','Rz')
        self._store(locals())

# Transversely isotropic materials.
class TransIsoElastic(Material):
    "Adds fibers to a (hyper)elastic base material."
    def __init__(self, c3, c4, c5, lam_max, axis_func, base):
        self._store(locals())

# Orthotropic materials.
class OrthoMaterial(Material):
    """Base class for orthotropic materials, not including iso or trans-iso
    materials."""

class LinearOrthotropic(OrthoMaterial):
    def __init__(self, E1, E2, E3, G12, G23, G31, v12, v23, v31, axis_func):
        self._store(locals())

class FungOrthotropic(OrthoMaterial):
    def __init__(self, E1, E2, E3, G12, G23, G31, v12, v23, v31, c, k, axis_func):
        self._store(locals())



class AxisOrientation(object):
    """Base class for special material axis orientation objects.

    Axes are defined by callable objects.  The call should take a single
    Element object, and return a set of three mutually-orthogonal unit vectors
    describing the orientation of the material axes within the given Element.

    Arbitrary callable objects can be used for axis orientation; special
    objects are used to identify special cases that solvers may have built-in."""

    def __init__(self, pos1, pos2):
        p = iter(pos1)
        self.pos1 = [p.next(), p.next(), p.next()]
        p = iter(pos2)
        self.pos2 = [p.next(), p.next(), p.next()]

    @staticmethod
    def _normalize(v1, v2):
        """Takes two vectors and returns three normalized unit vectors
        describing the corresponding axes.
        e1 = v1 / abs(v1), e2 = e3 x e1, e3 = (v1 x v2) / abs(v1 x v2)"""
        # All to avoid a numpy dependency...
        from math import sqrt
        absv1 = sqrt( sum(i*i for i in v1) )
        e1 = [i/absv1 for i in v1]

        v1xv2 = [
            v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0],
        ]
        absv1xv2 = sqrt( sum(i*i for i in v1xv2) )
        e3 = [i/absv1xv2 for i in v1xv2]

        e2 = [
            e3[1]*e1[2] - e3[2]*e1[1],
            e3[2]*e1[0] - e3[0]*e1[2],
            e3[0]*e1[1] - e3[1]*e1[0],
        ]

        return (e1, e2, e3)


class VectorOrientation(AxisOrientation):
    """Gives constant material axes throughout the entire domain.
    pos1 gives the primary axis, while pos2 indicates the direction of the
    secondary axis in the form:
    e1 = pos1 / abs(pos1), e2 = e3 x e1, e3 = (pos1 x pos2) / abs(pos1 x pos2)"""
    def __call__(self, element):
        return self._normalize(self.pos1, self.pos2)

class SphericalOrientation(AxisOrientation):
    """Gives primary material axes radiating outward from a central point.
    pos1 is the location of the central point.  pos2 is a vector indicating the
    direction of the secondary axis."""
    def __call__(self, element):
        v1 = [ e - p for e,p in zip(element.get_vertex_avg(), self.pos1) ]
        return self._normalize(v1, self.pos2)

class NodalOrientation(AxisOrientation):
    """Gives axes based on the positions of an Element's Nodes.
    edge1 and edge2 are each a pair of integers corresponding to 0-indexed node
    numbers.  Each element is given a primary axis in the direction of edge1,
    and a secondary axis based on the direction of edge2."""
    def __init__(self, edge1, edge2):
        # Where edge1 and edge2 are each a pair of integers corresponding to
        # element node indices.
        p = iter(edge1)
        self.edge1 = [p.next(), p.next()]
        p = iter(edge2)
        self.edge2 = [p.next(), p.next()]
        # NOTE: Orthotropic materials in FEBio expect edge1[0] == edge2[0].

    def __call__(self, element):
        v1 = [ element[ self.edge1[1] ][i] - element[ self.edge1[0] ][i]
            for i in xrange(3) ]
        v2 = [ element[ self.edge2[1] ][i] - element[ self.edge2[0] ][i]
            for i in xrange(3) ]
        return self._normalize(v1, v2)
