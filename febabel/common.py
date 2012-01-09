class Base(object):
    """The base class for all objects used in FEbabel.

    The get_children method is required in all FEbabel objects.  It should
    return a set containing all FEbabel objects contained by this object.  It
    should not contain any other objects (including None).  If this object has
    no children, it returns None (the default behaviour).
    Note that objects should only be contained in one direction, with no loops;
    this means that it should be safe to call get_children recursively on all
    children, sub-children, etc., without causing an infinite loop.
    
    The get_descendants method is also required, but will likely not need to be
    overridden by subclasses.  It returns a set containing all of the object's
    children, grandchildren, etc."""

    __slots__ = []

    def get_children(self):
        return None


    def get_descendants(self):
        children = self.get_children()
        if children is None:
            return set()

        descendants = set(children)
        for child in children:
            descendants.update(child.get_descendants())

        return descendants




class Constrainable(Base):
    """A mixin to allow different object types to accept constraints on each of
    its degrees of freedom."""

    __slots__ = ['constraints']

    def __init__(self, *degrees_of_freedom):
        self.constraints = dict( (i,None) for i in degrees_of_freedom )
        # TODO: Prevent new DOFs from being added after the fact.

    def get_children(self):
        s = set(self.constraints.itervalues())
        s.discard(None)
        return s




class Switch(Base):
    """A base for containers of other objects that can be activated or
    deactivated at specific times.

    points is a dict with numeric keys and values.  Each key represents a time,
    while its corresponding value represents the object activating at that
    time."""

    __slots__ = ['points']

    def __init__(self, points):
        self.points = points

    def get_children(self):
        s = set(self.points.itervalues())
        s.discard(None)
        return s


    # For more convenient read/write access to the points dictionary.
    def __getitem__(self, x):
        return self.points[x]

    def __setitem__(self, x, y):
        self.points[x] = y


    def get_active(self, time):
        """Find which contained object is active at the specified time.
        If the specified time is before the earliest specified time, None is
        returned."""
        # Iterate backwards through all given times to find the most recent.
        for t in sorted(self.points.iterkeys(), reverse=True):
            if t <= time:
                return self.points[t]
        return None
