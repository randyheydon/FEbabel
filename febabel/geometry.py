class Node(object):
    """A single point in three-dimensional Cartesian space.
    The node coordinates can be accessed and set through properties x,y,z.
    Similarly, coordinates can be indexed and iterated over like a list."""

    def __init__(self, pos):
        """Create a node at the given position.
        pos must be an iterable of length 3."""
        self._pos = list(pos)[0:3]

    @property
    def x(self):
        return self._pos[0]
    @x.setter
    def x(self, value):
        self._pos[0] = value

    @property
    def y(self):
        return self._pos[1]
    @y.setter
    def y(self, value):
        self._pos[1] = value

    @property
    def z(self):
        return self._pos[2]
    @z.setter
    def z(self, value):
        self._pos[2] = value


    def __iter__(self):
        return iter(self._pos)

    def __getitem__(self, i):
        return self._pos[i]

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._pos))
