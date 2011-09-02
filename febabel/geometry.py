class Node(object):
    """A single point in three-dimensional Cartesian space.
    The node coordinates can be accessed and set through properties x,y,z.
    Similarly, coordinates can be indexed and iterated over like a list."""

    def __init__(self, pos):
        """Create a node at the given position.
        pos must be an iterable of length 3."""
        self._pos = list(pos)[0:3]


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

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._pos))
