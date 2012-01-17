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


class Force(Constraint):
    def __repr__(self):
        return 'free' if self is free else Constraint.__repr__(self)
class Displacement(Constraint):
    def __repr__(self):
        return 'fixed' if self is fixed else Constraint.__repr__(self)
# Whenever possible, use these instances rather than creating new Force or
# Displacement instances.  This will allow for more efficient solutions.
free = Force(loadcurve_zero, 0)
fixed = Displacement(loadcurve_zero, 0)


class SwitchConstraint(Switch, Constraint):
    """Acts as a container for Constraint objects that change with time, while
    presenting itself as a Constraint object.

    Its default object, returned for get_active before the first set point, is
    the free constraint."""
    default = free




class Contact(Base):
    """Base class for a contact interface between two surface sets.

    master and slave are both iterables containing SurfaceElements."""

    def __init__(self, master, slave, options=None):
        self.master = set(master)
        self.slave = set(slave)
        self.options = options if options is not None else dict()

    def get_children(self):
        return self.master.union(self.slave)


class SlidingContact(Contact):
    """Contact interface between two surfaces that can slide and separate."""
    # TODO: Maybe break into separate friction, biphasic, and solute classes?

    def __init__(self, master, slave, friction_coefficient=0, biphasic=False,
                 solute=False, options=None):
        self.friction_coefficient = friction_coefficient
        self.biphasic = biphasic
        self.solute = solute
        Contact.__init__(master, slave, options)


class TiedContact(Contact):
    """Contact interface between two surfaces that cannot separate."""


class RigidInterface(Contact):
    """Contact interface between a set of nodes and the rigid body to which
    they are affixed in relative location."""
    def __init__(self, rigid_body, nodes):
        self.rigid_body = rigid_body
        self.nodes = set(nodes)

    def get_children(self):
        return self.nodes.union([self.rigid_body])


# TODO: Rigid wall, rigid joint.


class SwitchContact(Switch, Contact):
    """Acts as a container for Contact objects that change with time, while
    presenting itself as a Contact object."""
