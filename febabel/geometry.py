from .constraints import Constrainable

class Node(Constrainable):
    """A single point in three-dimensional Cartesian space.
    The node coordinates can be accessed and set through properties x,y,z.
    Similarly, coordinates can be indexed and iterated over like a list."""

    # Only one piece of data needs storing, so use slots to decrease memory.
    __slots__ = ['_pos']


    def __init__(self, pos, **kwargs):
        """Create a node at the given position.
        pos must be an iterable of length 3.
        NOTE: This will not protect you from yourself!  Insert *only* valid
        data (length 3 sequence of ints/floats), or the result will be
        undefined!"""
        p = iter(pos)
        self._pos = [p.next(), p.next(), p.next()]
        super(Node, self).__init__(**kwargs)


    # Special properties getters/setters.
    def _getx(self):
        return self._pos[0]
    def _setx(self, value):
        self._pos[0] = value
    x = property(_getx, _setx)

    def _gety(self):
        return self._pos[1]
    def _sety(self, value):
        self._pos[1] = value
    y = property(_gety, _sety)

    def _getz(self):
        return self._pos[2]
    def _setz(self, value):
        self._pos[2] = value
    z = property(_getz, _setz)


    # So a Node object can be treated like a list.
    def __iter__(self):
        return iter(self._pos)
    def __getitem__(self, i):
        return self._pos[i]
    def __setitem__(self, i, value):
        self._pos[i] = value
    def __len__(self):
        # Could return len(self._pos), but it will always be 3...
        return 3

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._pos))



class Element(object):
    "Base class for all different element types."

    def __init__(self, nodes, material=None, **kwargs):
        """nodes is an iterable of Node objects.
        material is a Material object, or None."""
        self._nodes = list(nodes)
        self._material = material
        super(Element, self).__init__(**kwargs)


class Tet4(Element):
    "4-node linear tetrahedral element."
class Pent6(Element):
    "6-node linear pentahedral (triangular prism) element."
class Hex8(Element):
    "8-node linear hexahedral (brick) element."
# TODO: Shells need thickness.
class Shell3(Element):
    "3-node triangular shell element."
class Shell4(Element):
    "4-node quadrilateral shell element."
class Spring(Element):
    "2-node tension-only element."
