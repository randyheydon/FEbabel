from .common import Base, Switch



class LoadCurve(Base):
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


    # For more convenient read/write access to the points dictionary.
    def __getitem__(self, x):
        return self.points[x]

    def __setitem__(self, x, y):
        self.points[x] = y


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




class Constraint(Base):
    "Base class for different types of constraints/loads."

    def __init__(self, loadcurve, multiplier=1):
        self.multiplier = multiplier
        self.loadcurve = loadcurve

    def get_children(self):
        return set([self.loadcurve])


class Force(Constraint): pass
class Displacement(Constraint): pass
# FIXME: Single instance of Fixed (and Free?)
class Fixed(Displacement):
    def __init__(self):
        Displacement.__init__(self, loadcurve_zero, 0)


class SwitchConstraint(Switch, Constraint):
    """Acts as a container for Constraint objects that change with time, while
    presenting itself as a Constraint object."""




class Contact(Base):
    """Defines a contact interface between two surface sets."""

    def __init__(self, master, slave):
        self.master = master
        self.slave = slave

    def get_children(self):
        # TODO, once API is settled here.
        pass


class SwitchContact(Switch, Contact):
    """Acts as a container for Contact objects that change with time, while
    presenting itself as a Contact object."""
