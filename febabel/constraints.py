class Constrainable(object):
    """A mixin to allow different object types to accept constraints on each of
    its degrees of freedom."""

    __slots__ = ['constraints']

    def __init__(self, *degrees_of_freedom):
        self.constraints = dict( (i,None) for i in degrees_of_freedom )
        # TODO: Prevent new DOFs from being added after the fact.



class Switch(object):
    """A mixin to help create a container for other objects that can be activated
    or deactivated at specific times.

    points is a dict with numeric keys and values.  Each key represents a time,
    while its corresponding value represents the object activating at that
    time."""

    def __init__(self, points):
        self.points = points

    def get_active(self, time):
        """Find which contained object is active at the specified time.
        If the specified time is before the earliest specified time, None is
        returned."""
        # Iterate backwards through all given times to find the most recent.
        for t in sorted(self.points.iterkeys(), reverse=True):
            if t <= time:
                return self.points[t]
        return None




class LoadCurve(object):
    """Defines how a constraint (load, displacement, etc.) varies with time.

    points is a dict with numeric keys and values.  Each key represents a time,
    while its corresponding value represents the constraint's value.

    interpolation and extrapolation define how the curve behaves between and
    beyond the given points, respectively.  Valid values for each are contained
    in this class; all IN_* values can be used for interpolation, EX_* for
    extrapolation."""

    IN_LINEAR = 'linear'
    IN_STEP = 'step'
    IN_CUBIC_SPLINE = 'spline'

    EX_CONSTANT = 'constant'
    EX_TANGENT = 'tangent'
    EX_REPEAT = 'repeat'
    EX_REPEAT_OFFSET = 'repeat offset'

    def __init__(self, points, interpolation=IN_LINEAR, extrapolation=EX_CONSTANT):
        self.points = points
        self.interpolation = interpolation
        self.extrapolation = extrapolation

    # TODO: Call object with a specific time to receive the loadcurve's value
    # at that time.
    #def __call__(self, time):
    #    point_times = self.points.keys()
    #    point_times.sort()

    #    if point_times[0] <= time <= point_times[-1]:
    #        if self.interpolation == self.IN_LINEAR:
    #            pass
    #        elif self.interpolation == self.IN_STEP:
    #            pass
    #        elif self.interpolation == self.IN_CUBIC_SPLINE:
    #            pass
    #        else:
    #            pass

    #    else:
    #        if self.extrapolation == self.EX_CONSTANT:
    #            return self.points[ point_times[0 if time <= point_times[0] else -1] ]
    #        elif self.extrapolation == self.EX_TANGENT:
    #            pass
    #        elif self.extrapolation == self.EX_REPEAT:
    #            return self( time % points_time[-1] )
    #        elif self.extrapolation == self.EX_REPEAT_OFFSET:
    #            pass
    #        else:
    #            pass


# A few common loadcurves.
loadcurve_zero = LoadCurve({0:0, 1:0})
loadcurve_constant = LoadCurve({0:1, 1:1})
loadcurve_ramp = LoadCurve({0:0, 1:1})




class Constraint(object):
    "Base class for different types of constraints/loads."

    def __init__(self, loadcurve, multiplier=1):
        self.multiplier = multiplier
        self.loadcurve = loadcurve


class Force(Constraint): pass
class Displacement(Constraint): pass
class Fixed(Displacement):
    def __init__(self):
        Displacement.__init__(self, loadcurve_zero, 0)


class SwitchConstraint(Switch, Constraint):
    """Acts as a container for Constraint objects that change with time, while
    presenting itself as a Constraint object."""




class Contact(object):
    """Defines a contact interface between two surface sets."""

    def __init__(self, master, slave):
        self.master = master
        self.slave = slave


class SwitchContact(Switch, Contact):
    """Acts as a container for Contact objects that change with time, while
    presenting itself as a Contact object."""
